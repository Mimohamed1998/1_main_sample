"""Pipeline script for K-Means clustering.

Reads configuration from ``conf/variables.yaml`` and ``conf/paths.yaml``,
loads the input dataset, runs elbow analysis, performs clustering, and
produces cluster-average CSV files.
"""

import sys
from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Project root setup – same pattern used by the other pipeline scripts.
# ---------------------------------------------------------------------------
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.config import load_yaml_config
from src.utils.logger import get_logger
from src.tools.kmeans_clustering import KMeansClustering

logger = get_logger(__name__)


def main():
    """Runs the full K-Means clustering pipeline.

    Steps:
        1. Load configuration (paths and variables).
        2. Read the input CSV dataset.
        3. Run elbow analysis and save the elbow plot.
        4. Fit K-Means with the selected k.
        5. Save three cluster-average CSV files and the clustered raw data.
    """
    logger.info("Starting K-Means Clustering Pipeline...")

    # ------------------------------------------------------------------
    # 1. Load configuration
    # ------------------------------------------------------------------
    paths_cfg = load_yaml_config("paths.yaml")
    vars_cfg = load_yaml_config("variables.yaml")

    kmeans_cfg = vars_cfg["kmeans"]
    k_range = tuple(kmeans_cfg["k_range"])
    selected_k = kmeans_cfg["selected_k"]
    clustering_features = kmeans_cfg["clustering_features"]
    profiling_features = kmeans_cfg["profiling_features"]
    standardize = kmeans_cfg.get("standardize", True)

    output_dir = project_root / paths_cfg["kmeans_output"]
    output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # 2. Load data – default to processed data; override via paths.yaml
    # ------------------------------------------------------------------
    input_path_key = paths_cfg.get("kmeans_input", paths_cfg.get("processed_data"))
    input_dir = project_root / input_path_key

    # Find the first CSV in the input directory
    csv_files = sorted(input_dir.glob("*.csv"))
    if not csv_files:
        logger.error(f"No CSV files found in {input_dir}")
        return

    input_file = csv_files[0]
    logger.info(f"Using input file: {input_file.name}")
    df = pd.read_csv(input_file)
    logger.info(f"Loaded dataset with shape: {df.shape}")

    # ------------------------------------------------------------------
    # 3. Elbow analysis
    # ------------------------------------------------------------------
    logger.info(f"Running elbow analysis for k = {k_range[0]}..{k_range[1]}")
    inertias = KMeansClustering.run_elbow_analysis(
        df=df,
        features=clustering_features,
        k_range=k_range,
        output_path=output_dir,
        standardize=standardize,
    )
    for k, inertia in inertias.items():
        logger.debug(f"  k={k}  inertia={inertia:.2f}")

    logger.info(f"Elbow plot saved to {output_dir / 'elbow_plot.png'}")

    # ------------------------------------------------------------------
    # 4. Cluster with selected k
    # ------------------------------------------------------------------
    logger.info(f"Fitting K-Means with k={selected_k}")
    df_clustered = KMeansClustering.run_clustering(
        df=df,
        features=clustering_features,
        k=selected_k,
        standardize=standardize,
    )
    logger.info(
        f"Cluster distribution:\n"
        f"{df_clustered['cluster'].value_counts().sort_index().to_string()}"
    )

    # ------------------------------------------------------------------
    # 5. Cluster profiles
    # ------------------------------------------------------------------
    all_features = clustering_features + profiling_features

    # 5a. Clustering features averages
    clustering_profiles = KMeansClustering.get_cluster_profiles(
        df_clustered, clustering_features
    )
    clustering_csv = output_dir / "clustering_features_averages.csv"
    clustering_profiles.to_csv(clustering_csv, index=False)
    logger.info(f"Clustering feature averages saved to {clustering_csv.name}")

    # 5b. Profiling features averages
    profiling_profiles = KMeansClustering.get_cluster_profiles(
        df_clustered, profiling_features
    )
    profiling_csv = output_dir / "profiling_features_averages.csv"
    profiling_profiles.to_csv(profiling_csv, index=False)
    logger.info(f"Profiling feature averages saved to {profiling_csv.name}")

    # 5c. All features averages
    all_profiles = KMeansClustering.get_cluster_profiles(
        df_clustered, all_features
    )
    all_csv = output_dir / "all_features_averages.csv"
    all_profiles.to_csv(all_csv, index=False)
    logger.info(f"All feature averages saved to {all_csv.name}")

    # 5d. Clustered raw data
    clustered_data_csv = output_dir / "clustered_data.csv"
    df_clustered.to_csv(clustered_data_csv, index=False)
    logger.info(f"Clustered raw data saved to {clustered_data_csv.name}")

    logger.info("K-Means Clustering Pipeline completed successfully!")


if __name__ == "__main__":
    main()
