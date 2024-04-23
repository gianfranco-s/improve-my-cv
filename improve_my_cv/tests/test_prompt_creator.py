import json

from improve_my_cv.prompt_handler.prompt_creator import PromptCreator
from improve_my_cv.tests import valid_resume


def test_prompt_creator_create_prompt_with_valid_strings(valid_resume: dict) -> None:
    prompt_template = "Here's the JD {job_description}\nand here's the resume {json_resume}"
    job_description = 'An astronaut with 50 years experience'

    prompt_creator = PromptCreator(prompt_template=prompt_template,
                                   job_description=job_description,
                                   json_resume=valid_resume,
                                   apply_field_filters=False)

    full_prompt = prompt_creator.create_prompt()

    assert full_prompt == prompt_template.format(job_description=job_description,
                                                 json_resume=json.dumps(valid_resume, indent=4))
