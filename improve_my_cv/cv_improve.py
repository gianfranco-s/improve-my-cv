import json

from improve_my_cv.llm_handlers.base_handler import LLMHandler
from improve_my_cv.log_config import logger
from improve_my_cv.prompt_handler.prompt_creator import PromptCreator


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
        prompt_creator = PromptCreator(json_resume=self.original_resume, job_description=job_description)
        self.prompt = prompt_creator.create_prompt()
        self.filtered_resume = prompt_creator.filtered_json_resume

        self.improved_resume: dict = None
        self.model: str = None
        self.llm_handler: LLMHandler = None
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
            raise InvalidResponseException('LLM returned an invalid format for response\n'
                                           f'{e}\ntype:{type(model_response.text)}\n'
                                           f'{model_response.text}')

        logger.info('Done')
        return self.improved_resume

    def response_warnings(self) -> dict | None:
        """Check if static values like field names have changed."""
        field_names_changed = self._field_names_changed(self.filtered_resume, self.improved_resume)

        if len(field_names_changed) > 0:
            return {
                'field_names_changed': field_names_changed,
            }

    @staticmethod
    def _field_names_changed(original: dict, improved: dict) -> set:
        """
        Identifies field names that are different between the original and improved resumes.

        Returns:
            A set containing the field names that exist in either the original or
            improved resume but not both (i.e., the difference between the field name sets).
        """

        original_field_names = set(original.keys())
        new_field_names = set(improved.keys())

        changed_fields = original_field_names.symmetric_difference(new_field_names)

        return changed_fields
