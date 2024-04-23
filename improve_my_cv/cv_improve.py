import json

from improve_my_cv.llm_handlers.base_handler import LLMHandler
from improve_my_cv.log_config import logger
from improve_my_cv.post_processor.resume_rebuild import ResumeRebuilder
from improve_my_cv.prompt_handler.prompt_creator import PromptCreator
from improve_my_cv.utils import are_keys_the_same


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

    def improve_cv(self, rebuild_resume: bool = True) -> dict:
        self.llm_setup(self.model, self.llm_handler)
        logger.info(f'Attempting to improve resume with model {self.model}')
        self.llm_handler.generate(prompt=self.prompt, model=self.model)
        model_response = self.llm_handler.standardize_response()

        try:
            improved_resume = json.loads(model_response.text)

            if not isinstance(improved_resume, dict):
                raise InvalidResponseException(f'LLM returned an invalid format for response\n{self.improved_resume}')

        except json.decoder.JSONDecodeError as e:
            raise InvalidResponseException('LLM returned an invalid format for response\n'
                                           f'{e}\ntype:{type(model_response.text)}\n'
                                           f'{model_response.text}')

        logger.info('Done')
        if rebuild_resume:
            rebuilder = ResumeRebuilder(original_resume=self.original_resume, filtered_resume=improved_resume)
            self.improved_resume = rebuilder.rebuild()
        else:
            logger.warning('If resume is not rebuilt properly, some fields may not appear in the final version.')
            self.improved_resume = improved_resume

        return self.improved_resume

    def response_warnings(self) -> dict | None:
        """Check if static values like field names have changed."""
        field_names_changed = not are_keys_the_same(self.filtered_resume, self.improved_resume)

        if field_names_changed:
            return {
                'field_names_changed': field_names_changed,
            }
