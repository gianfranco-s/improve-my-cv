import json

from improve_my_cv.llm_handler import LLMHandler, HandleOllama
from improve_my_cv.prompt_creator import PromptCreator

DEFAULT_MODEL = 'llama2'
DEFAULT_LLMHANDLER = HandleOllama()


class InvalidResponseException(Exception):
    pass


class InvalidResumeInputException(Exception):
    pass


class ImproveMyCV:
    """Receives a dictionary of the original resume and, based on the JD, returns an improved resume."""
    def __init__(self, original_resume: dict, job_description: str) -> None:
        if not isinstance(original_resume, dict):
            raise InvalidResumeInputException('Resume must be dict')

        self.original_resume = original_resume
        self.prompt = PromptCreator(json_resume=json.dumps(self.original_resume), job_description=job_description).create_prompt()
        self.improved_resume: dict = None

    def improve_cv(self, model: str = DEFAULT_MODEL, llm_handler: LLMHandler = DEFAULT_LLMHANDLER, perform_checks: bool = True) -> dict:
        llm_handler.generate(prompt=self.prompt, model=model)
        model_response = llm_handler.standardize_response()

        self.improved_resume = json.loads(model_response.text)

        if perform_checks:
            self.perform_response_checks()

        return self.improved_resume

    def _check_improved_resume_is_dict(self) -> None:
        if not isinstance(self.improved_resume, dict):
            raise InvalidResponseException(f'LLM returned non-JSON response:\n{self.improved_resume}')

    def _check_unchanged_field_names(self) -> None:
        original_field_names = set(self.original_resume.keys())
        new_field_names = set(self.improved_resume.keys())

        if original_field_names != new_field_names:
            raise InvalidResponseException('Some field names have been changed in the response:\n{self.improved_resume}')

    def _check_unchanged_dates(self) -> None:
        date_fields_changed = []

        for key in self.original_resume:
            if 'date' in key.lower() and key in self.improved_resume:
                if self.original_resume[key] != self.improved_resume[key]:
                    date_fields_changed.append(key)

        if len(date_fields_changed) > 0:
            raise InvalidResponseException('Some dates have been changed on the resume:\n{self.improved_resume}')

    def _check_unchanged_user_data(self) -> None:
        user_fields = {'name', 'email', 'phone', 'url', 'location', 'username'}

        user_fields_changed = []

        # TODO: apply this to deeply nested keys, as in urls within profiles
        for field in user_fields:
            if field in self.original_resume and field in self.improved_resume:
                if self.original_resume[field] != self.improved_resume[field]:
                    user_fields_changed.append(field)

        if len(user_fields_changed) > 0:
            raise InvalidResponseException('Some user data has been changed')

    def perform_response_checks(self) -> dict:
        self._check_improved_resume_is_dict()
        self._check_unchanged_field_names()
        self._check_unchanged_dates()
        self._check_unchanged_user_data()