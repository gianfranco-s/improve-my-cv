import json

from pathlib import Path

from improve_my_cv import resume_dir
from improve_my_cv.llm_handler import HandleOllama


def load_json_resume(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    resume = load_json_resume(resume_dir / 'example_cv.json')
    handler = HandleOllama()
    handler.generate(prompt='why is the sky blue?')
    response = handler.standardize_response()
    print(response)
