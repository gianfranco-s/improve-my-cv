import json
from dataclasses import dataclass

from improve_my_cv.log_config import logger
from improve_my_cv.prompt_handler.cv_fields_filter import filter_resume


@dataclass
class PromptCreator:
    job_description: str
    json_resume: dict
    filtered_json_resume: dict = None
    apply_field_filters: bool = True
    prompt_template: str = (
        "You are a robot that only outputs JSON objects. "
        "Your role is of an experienced recruiter. "
        "Your job is to improve a current resume with relevant words from a job description. "
        "You'll be given two parameters and their values. "
        "Parameter names will be surrounded by one backtick. Example: `this_is_a_parameters_name`. "
        "Parameter values will be provided directly after the colon, not surrounded by backticks. "
        "**Identify relevant keywords** from the job description, "
        "**and then incorporate these keywords by rewriting existing content to better reflect my qualifications.** "
        "Please only answer with a modified JSON, based on `json_resume`. "
        "Answer should be a correctly formatted JSON object. "
        "Do not provide any other explanation, outside the JSON response. "
        "Do not change any field names. "
        "Do not add any field names. "
        "Only answer in english. "
        "`job_description`\n{job_description}\n"
        "`json_resume`\n{json_resume}\n"
    )

    def __post_init__(self):
        if self.apply_field_filters:
            self.filtered_json_resume = filter_resume(self.json_resume)
        else:
            logger.warning("Please note that LLM may change")
            logger.warning("- user's data, like name or address")
            logger.warning("- static data, like dates or urls")
            logger.warning("- JSON field names.")

    def create_prompt(self) -> str:
        json_resume = self.filtered_json_resume if self.apply_field_filters else self.json_resume
        return self.prompt_template.format(job_description=self.job_description,
                                           json_resume=json.dumps(json_resume, indent=4))
