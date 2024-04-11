import json

from improve_my_cv.llm_handler import LLMHandler, HandleOllama
from improve_my_cv.prompt_creator import PromptCreator

DEFAULT_MODEL = 'llama2'
DEFAULT_LLMHANDLER = HandleOllama()
class InvalidResponseException(Exception):
    pass


class ImproveMyCV:
    def __init__(self, original_resume: str, job_description: str) -> None:
        self.original_resume = json.loads(original_resume)
        self.prompt = PromptCreator(json_resume=self.original_resume, job_description=job_description).create_prompt()
        self.improved_resume: dict = None
        self.improved_text_resume: str = None

    def improve_cv(self, model: str = DEFAULT_MODEL, llm_handler: LLMHandler = DEFAULT_LLMHANDLER) -> str:
        llm_handler.generate(prompt=self.prompt, model=model)
        model_response = llm_handler.standardize_response()

        self.improved_resume = model_response.text
        self._check_improved_resume_is_dict()
        self._check_unchanged_field_names()
        self._check_unchanged_dates()

        self.improved_text_resume = json.dumps(self.improved_resume)

        return self.improved_text_resume

    def _check_improved_resume_is_dict(self) -> None:
        if not isinstance(self.improved_resume, dict):
            raise InvalidResponseException('LLM returned non-JSON response')

    def _check_unchanged_field_names(self) -> None:
        original_field_names = set(self.original_resume.keys())
        new_field_names = set(self.improved_resume.keys())

        if original_field_names != new_field_names:
            raise InvalidResponseException('Some field names have been changed in the response')

    def _check_unchanged_dates(self) -> None:
        date_fields_changed = []
        
        for key in self.original_resume:
            if 'date' in key.lower() and key in self.improved_resume:
                if self.original_resume[key] != self.improved_resume[key]:
                    date_fields_changed.append(key)

        if len(date_fields_changed) > 0:
            raise InvalidResponseException('Some dates have been changed on the resume')


    def _check_unchanged_user_data(self) -> None:
        pass
