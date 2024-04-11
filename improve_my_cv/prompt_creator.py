from dataclasses import dataclass


@dataclass
class PromptCreator:
    job_description: str
    json_resume: str
    prompt_template: str

    def create_prompt(self) -> str:
        pass


class ImproveMyCV:
    pass