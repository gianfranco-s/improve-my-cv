import json

from improve_my_cv.llm_handler import LLMHandler


class InvalidResponseException(Exception):
    pass


class ImproveMyCV:
    def __init__(self, original_resume: str) -> None:
        self.original_resume = json.loads(original_resume)

    def improve_cv(self, prompt: str, llm_handler: LLMHandler) -> str:
        pass

    def _check_improved_resume_is_json_like(self) -> None:
        pass

    def _check_unchanged_field_names(self) -> None:
        pass

    def _check_unchanged_dates(self) -> None:
        pass

    def _check_unchanged_user_data(self) -> None:
        pass
