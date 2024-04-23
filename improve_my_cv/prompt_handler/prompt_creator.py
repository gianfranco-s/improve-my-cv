import json

from dataclasses import dataclass

from improve_my_cv.prompt_handler.cv_fields_filter import filter_resume


@dataclass
class PromptCreator:
    job_description: str
    json_resume: str
    prompt_template: str = "You are a robot that only outputs JSON objects. " \
        "Your role is an experienced recruiter, who improves a current resume with relevant words from a job description. " \
        "You'll be given two parameters and their values. " \
        "Parameter names will be surrounded by one backtick. Example: `this_is_a_parameters_name`. " \
        "Parameter values will be provided directly after the colon, not surrounded by backticks. " \
        "**Identify relevant keywords** from the job description, " \
        "**and then incorporate these keywords by rewriting existing content in these fields to better reflect my qualifications for the job described.**" \
        "Please only answer with a modified JSON, based on `json_resume`" \
        "Answer should be a correctly formatted JSON object" \
        "Do not provide any other explanation, outside the JSON response" \
        "Do not change any field names" \
        "`job_description` {job_description}" \
        "`json_resume` {json_resume}" 

    def create_prompt(self) -> str:
        resume = filter_resume(self.json_resume)
        return self.prompt_template.format(job_description=self.job_description,
                                           json_resume=json.dumps(resume, indent=4))
