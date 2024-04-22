# Improve My CV
This project is designed to use LLMs to improve a json-resume based on a particular string-job-description.

## To run the project
1. [Install Ollama](https://ollama.com/download)
2. Install dependencies
   ```
   poetry install
   ```
   
3. To run the project
   Run the script from the project's root dir

   ### Using the CLI
   ```
   python3 -m improve_my_cv.ui_cli
   ```

   ### Using Streamlit (in a browser)
   ```
   streamlit run improve_my_cv/ui_streamlit.py
   ```

## Useful documentation for development
https://github.com/ollama/ollama/blob/main/docs/api.md
