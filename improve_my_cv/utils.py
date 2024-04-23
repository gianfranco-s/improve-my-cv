import json
from pathlib import Path

from deepdiff import DeepDiff

from improve_my_cv.log_config import logger


def load_json_resume(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


def save_operations(improved_cv: dict, filename: str) -> None:
    logger.info(f'Saving to file {filename}')

    with open(filename, 'w') as f:
        json.dump(improved_cv, f, indent=4)


def are_keys_the_same(dict1: dict, dict2: dict) -> bool:
    diff = DeepDiff(dict1, dict2, ignore_order=True)

    if 'dictionary_item_added' in diff or 'dictionary_item_removed' in diff:
        return False  # If dictionaries were added or removed, keys are not the same

    nested_diffs = diff.get('values_changed', [])

    for nested_diff in nested_diffs:
        if 'new_value' in nested_diff or 'old_value' in nested_diff:
            return False  # If values were changed within nested dictionaries, keys are not the same

    return True
