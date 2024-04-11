import json

from pathlib import Path

from improve_my_cv.llm_handler import HandleOllama


def load_json_resume(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    resume_dir = Path(__file__).parents[1] / 'json_cv'
    resume = load_json_resume(resume_dir / 'example_cv.json')
    handler = HandleOllama()
    response = handler.generate(prompt='why is the sky blue?')

    print(response)
