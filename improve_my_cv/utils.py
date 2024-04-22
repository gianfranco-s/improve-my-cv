import json

from pathlib import Path

from improve_my_cv.log_config import logger


def load_json_resume(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


def save_operations(improved_cv: dict, filename: str) -> None:
    logger.info(f'Saving to file {filename}')

    with open(filename, 'w') as f:
        json.dump(improved_cv, f, indent=4)
