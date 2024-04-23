from improve_my_cv import resume_dir
from improve_my_cv.cv_improve import ImproveMyCV
from improve_my_cv.llm_handlers.ollama import DEFAULT_OLLAMA_MODEL, HandleOllama
from improve_my_cv.log_config import logger
from improve_my_cv.utils import load_json_resume, save_operations

job_description = """
    Example job description:

    About the job
    Python Developer

    We are looking for a skilled freelance Python developer to join our team on a project basis.

    Requirements:
    Proficiency in Python programming language
    Experience with web development frameworks like Django or Flask

    Nice to have:
    Experience with database systems (e.g., MySQL, PostgreSQL)
    Knowledge of version control systems (e.g., Git)
    Familiarity with Agile development methodologies
    """


def manual_interface():

    resume = load_json_resume(resume_dir / 'example_cv.json')

    improve = ImproveMyCV(original_resume=resume, job_description=job_description)
    improve.llm_setup(model=DEFAULT_OLLAMA_MODEL, llm_handler=HandleOllama())
    improved_cv = improve.improve_cv()

    warnings = improve.response_warnings()
    if warnings:
        logger.warning(warnings)

    filename = 'improved_cv.json'
    save_operations(improved_cv=improved_cv, filename=filename)


if __name__ == "__main__":
    manual_interface()
