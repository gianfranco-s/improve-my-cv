import json

from pathlib import Path

from improve_my_cv import resume_dir
from improve_my_cv.cv_improve import ImproveMyCV


def load_json_resume(filepath: Path) -> str:
    with open(filepath, 'r') as f:
        return json.dumps(json.load(f))


if __name__ == '__main__':
    resume = load_json_resume(resume_dir / 'example_cv.json')
    job_description = """
    About the job
    Python Developer

    We are looking for a skilled freelance Python developer to join our team on a project basis. The ideal candidate should have experience in Python programming, including web development frameworks such as Django or Flask. Responsibilities will include developing and maintaining Python-based applications, collaborating with team members to define project requirements, and ensuring code quality and performance. This is a remote position with flexible hours.

    Requirements:
    Proficiency in Python programming language
    Experience with web development frameworks like Django or Flask
    Familiarity with front-end technologies (HTML, CSS, JavaScript)
    Strong problem-solving skills and attention to detail
    Ability to work independently and meet project deadlines
    Excellent communication and collaboration skills

    Nice to have:
    Experience with database systems (e.g., MySQL, PostgreSQL)
    Knowledge of version control systems (e.g., Git)
    Familiarity with Agile development methodologies
    """

    improve = ImproveMyCV(original_resume=resume, job_description=job_description)
    improved_cv = improve.improve_cv()

    print(improved_cv)
