import json

from pathlib import Path

import streamlit as st

from improve_my_cv import resume_dir
from improve_my_cv.cv_improve import ImproveMyCV
from improve_my_cv.log_config import logger

job_description_placeholder = """
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


def load_json_resume(filepath: Path) -> dict:
    with open(filepath, 'r') as f:
        return json.load(f)


def save_operations(improved_cv: dict, filename: str) -> None:
    logger.info(f'Saving to file {filename}')

    with open(filename, 'w') as f:
        json.dump(improved_cv, f, indent=4)


def streamlit_ui():
    st.title("Improve My CV")

    job_description = st.text_area("Enter Job Description", height=200, placeholder=job_description_placeholder)
    uploaded_file = st.file_uploader("Upload your CV (JSON format)", type="json")

    if uploaded_file is not None and job_description:
        resume = json.load(uploaded_file)

        improve = ImproveMyCV(original_resume=resume, job_description=job_description)
        improved_cv = improve.improve_cv()

        warnings = improve.response_warnings()
        if warnings:
            logger.warning(warnings)
            st.warning(warnings)

        filename = 'improved_cv.json'
        save_operations(improved_cv=improved_cv, filename=filename)
        st.success(f"Improved CV has been saved to '{filename}'")


if __name__ == "__main__":
    streamlit_ui()
