import logging
from pathlib import Path


def setup_logging():
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logs_path = Path("logs/")

    if not logs_path.is_dir():
        logs_path.mkdir(exist_ok=True)

    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
