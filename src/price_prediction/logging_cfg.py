import logging
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Set up logging configuration.
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Default log file
    if log_file is None:
        log_file = log_dir / "price_prediction.log"

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)
