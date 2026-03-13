import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from typing import List, Tuple, Dict, Optional


class KMeansClustering:
    """Utility class for K-Means clustering analysis.

    Provides methods to run elbow analysis, fit a K-Means model for a
    chosen k, and compute cluster profile averages across feature sets.
    """

    @staticmethod
    def run_elbow_analysis(
        df: pd.DataFrame,
        features: List[str],
        k_range: Tuple[int, int],
        output_path: Path,
        standardize: bool = True,
    ) -> Dict[int, float]:
        """Runs K-Means for a range of k values and saves an elbow plot.

        Args:
            df: Input DataFrame containing the feature columns.
            features: List of column names to use for clustering.
            k_range: Tuple of (min_k, max_k) inclusive range to evaluate.
            output_path: Directory where the elbow plot PNG will be saved.
            standardize: Whether to standardise features before clustering.
                Defaults to True.

        Returns:
            A dictionary mapping each k value to its corresponding inertia
            (within-cluster sum of squares).

        Raises:
            ValueError: If any feature in *features* is missing from *df*.
        """
        missing = [f for f in features if f not in df.columns]
        if missing:
            raise ValueError(f"Features not found in DataFrame: {missing}")

        X = df[features].copy()

        if standardize:
            scaler = StandardScaler()
            X = pd.DataFrame(
                scaler.fit_transform(X), columns=features, index=X.index
            )

        k_values = range(k_range[0], k_range[1] + 1)
        inertias: Dict[int, float] = {}

        for k in k_values:
            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            model.fit(X)
            inertias[k] = model.inertia_

        # Plot
        plt.figure(figsize=(10, 6))
        plt.plot(list(inertias.keys()), list(inertias.values()), "bo-")
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia (Within-cluster Sum of Squares)")
        plt.title("Elbow Plot for K-Means Clustering")
        plt.xticks(list(inertias.keys()))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        plot_file = output_path / "elbow_plot.png"
        plt.savefig(plot_file, dpi=150)
        plt.close()

        return inertias

    @staticmethod
    def run_clustering(
        df: pd.DataFrame,
        features: List[str],
        k: int,
        standardize: bool = True,
    ) -> pd.DataFrame:
        """Fits K-Means with the specified k and appends a cluster column.

        Args:
            df: Input DataFrame containing the feature columns.
            features: List of column names to use for clustering.
            k: Number of clusters.
            standardize: Whether to standardise features before clustering.
                Defaults to True.

        Returns:
            A copy of *df* with an additional ``cluster`` column containing
            the assigned cluster label (integer starting from 0).

        Raises:
            ValueError: If any feature in *features* is missing from *df*.
        """
        missing = [f for f in features if f not in df.columns]
        if missing:
            raise ValueError(f"Features not found in DataFrame: {missing}")

        X = df[features].copy()

        if standardize:
            scaler = StandardScaler()
            X = pd.DataFrame(
                scaler.fit_transform(X), columns=features, index=X.index
            )

        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)

        result = df.copy()
        result["cluster"] = labels
        return result

    @staticmethod
    def get_cluster_profiles(
        df: pd.DataFrame,
        feature_list: List[str],
    ) -> pd.DataFrame:
        """Computes the mean of specified features for each cluster.

        The DataFrame must already contain a ``cluster`` column (e.g. as
        produced by :meth:`run_clustering`).

        Args:
            df: DataFrame that includes a ``cluster`` column and all columns
                listed in *feature_list*.
            feature_list: Column names whose cluster-level averages are
                required.

        Returns:
            A DataFrame indexed by ``cluster`` with one column per feature,
            containing cluster-level mean values.

        Raises:
            ValueError: If ``cluster`` column is missing or any feature in
                *feature_list* is not present in *df*.
        """
        if "cluster" not in df.columns:
            raise ValueError(
                "DataFrame must contain a 'cluster' column. "
                "Run run_clustering() first."
            )

        missing = [f for f in feature_list if f not in df.columns]
        if missing:
            raise ValueError(f"Features not found in DataFrame: {missing}")

        profiles = (
            df.groupby("cluster")[feature_list]
            .mean()
            .reset_index()
        )
        return profiles
