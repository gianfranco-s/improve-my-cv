import json

import streamlit as st

from improve_my_cv.cv_improve import ImproveMyCV
from improve_my_cv.llm_handlers.ollama import HandleOllama, DEFAULT_OLLAMA_MODEL
from improve_my_cv.log_config import logger
from improve_my_cv.utils import save_operations


def streamlit_ui(model: str = DEFAULT_OLLAMA_MODEL):
    st.title("Improve My CV")

    job_description = st.text_area("Enter Job Description", height=200, placeholder='Add a text job description here')
    uploaded_file = st.file_uploader("Upload your CV (JSON format)", type="json")

    if st.button("Improve!"):
        if uploaded_file is not None and job_description:
            resume = json.load(uploaded_file)

            improve = ImproveMyCV(original_resume=resume, job_description=job_description)
            improve.llm_setup(model=model, llm_handler=HandleOllama())

            st.write(f'Improving resume using model {model}')
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
