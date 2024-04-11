import json

from pathlib import Path

from improve_my_cv.llm_handler import get_llm_response

def load_json_resume(filepath: Path):
    with open(filepath, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    resume = load_json_resume('cv_python_dev.json')
    print(resume)
