import logging
import sys

def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Creates and returns a configured logger.
    
    Args:
        name: The name of the logger, typically __name__ of the caller.
        level: The logging level. Defaults to logging.DEBUG to show all messages.
    
    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if the logger already exists
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        # Create message formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger
