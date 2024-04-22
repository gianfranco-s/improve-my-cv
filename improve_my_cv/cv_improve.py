import json

from improve_my_cv.llm_handlers.base_handler import LLMHandler
from improve_my_cv.log_config import logger
from improve_my_cv.prompt_creator import PromptCreator


class InvalidModelException(Exception):
    pass


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
        self.model = None
        self.llm_handler = None
        logger.debug(f'prompt: {self.prompt}')

    def llm_setup(self, model: str, llm_handler: LLMHandler) -> None:
        self.model = model
        self.llm_handler = llm_handler
        if self.model is None or self.llm_handler is None:
            raise InvalidModelException('You must select a model and llm_handler by running llm_setup()')
    
    def improve_cv(self) -> dict:
        self.llm_setup(self.model, self.llm_handler)
        logger.info(f'Attempting to improve resume with model {self.model}')
        self.llm_handler.generate(prompt=self.prompt, model=self.model)
        model_response = self.llm_handler.standardize_response()

        try:
            self.improved_resume = json.loads(model_response.text)

            if not isinstance(self.improved_resume, dict):
                raise InvalidResponseException(f'LLM returned an invalid format for response\n{self.improved_resume}')

        except json.decoder.JSONDecodeError as e:
            raise InvalidResponseException(f'LLM returned an invalid format for response\n{e}\ntype:{type(model_response.text)}\n{model_response.text}')

        logger.info('Done')
        return self.improved_resume

    def _field_names_changed(self) -> set:
        """
        Identifies field names that are different between the original and improved resumes.

        Returns:
            A set containing the field names that exist in either the original or
            improved resume but not both (i.e., the difference between the field name sets).
        """

        original_field_names = set(self.original_resume.keys())
        new_field_names = set(self.improved_resume.keys())

        changed_fields = original_field_names.symmetric_difference(new_field_names)

        return changed_fields

    def _dates_changed(self) -> dict:
        """
        Identifies field names that are different between the original and improved resumes.

        Returns:
            A set containing the field names that exist in either the original or
            improved resume but not both (i.e., the difference between the field name sets).
        """

        date_fields_changed = dict()

        for key in self.original_resume:
            if 'date' in key.lower() and key in self.improved_resume:
                original_date = self.original_resume[key]
                new_date = self.improved_resume[key]
                if original_date != new_date:
                    date_fields_changed.update({key: f'{original_date} -> {new_date}'})

        return date_fields_changed

    def _is_user_data_changed(self) -> bool:
        user_fields = {'name', 'email', 'phone', 'url', 'location', 'username'}

        user_fields_changed = []

        # TODO: apply this to deeply nested keys, as in urls within profiles
        for field in user_fields:
            if field in self.original_resume and field in self.improved_resume:
                original_value = self.original_resume[field]
                new_value = self.improved_resume[field]
                if original_value != new_value:
                    user_fields_changed.append((field, f'{original_value} -> {new_value}'))

        return len(user_fields_changed) > 0

    def response_warnings(self) -> dict | None:
        field_names_changed = self._field_names_changed()
        dates_changed = self._dates_changed()
        is_user_data_changed = self._is_user_data_changed()

        if any((len(field_names_changed) > 0, len(dates_changed) > 0, is_user_data_changed)):
            return {
                'field_names_changed': field_names_changed,
                'dates_changed': dates_changed,
                'is_user_data_changed': is_user_data_changed,
            }
