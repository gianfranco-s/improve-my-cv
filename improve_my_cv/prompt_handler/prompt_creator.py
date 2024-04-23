from dataclasses import dataclass


from improve_my_cv.prompt_handler.cv_fields_filter import filter_resume


@dataclass
class PromptCreator:
    job_description: str
    json_resume: str
    prompt_template: str = """
        You are a robot that only outputs JSON objects.
        Your role is a reviewer, which improves a current resume with relevant words from a job description.

        You'll be given two parameters and their values.
        Parameter names will be surrounded by one backtick. Example: `this_is_a_parameters_name`.
        Parameter values will be provided directly after the colon, not surrounded by backticks.

        The first parameter, `job_description`, is a job description text. The second parameter, `json_resume`, is a resume in the JSON format.

        Please update the following sections of `json_resume`'s fields to better match the `job_description`: "label", "work", "skills", "interests", "projects", "summary"
        **Identify relevant keywords** from the job description,
        **and then incorporate these keywords by rewriting existing content in these fields to better reflect my qualifications for the job described.**

        Please only answer with a modified JSON, based on `json_resume`
        Answer should be a correctly formatted JSON object
        Do not provide any other explanation, outside the JSON response
        Do not change any field names
        Do not change any values in the following fields: "name", "email", "phone", "url", "location", "profiles", "education", "certificates", "publications", "languages"

        `job_description`:
            {job_description}

        `json_resume`:
            {json_resume}

        """

    def create_prompt(self) -> str:
        return self.prompt_template.format(job_description=self.job_description,
                                           json_resume=filter_resume(self.json_resume))
