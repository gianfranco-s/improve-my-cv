from dataclasses import dataclass


@dataclass
class PromptCreator:
    job_description: str
    json_resume: str
    prompt_template: str = """
        You'll be given two parameters: `job_description` and a `json_resume`. The first one is a job description text. The latter is a resume in the JSON format.
        Please update the following sections of `json_resume`'s fields to better match the `job_description`: "work", "skills", "interests", "projects", "summary", "label"
        **by including relevant keywords** from the job description.
        
        Please only answer with an modified JSON, based on `json_resume`
        Do not provide any other explanation, outside the JSON response
        Do not change any field names
        Do not change any values for the following fields: "name", "email", "phone", "url", "location", "profiles", "education", "certificates", "publications", "languages"
        Each parameter's value will be delimited by the characters ```

        `job_description`:
        ```
        {job_description}
        ```

        `json_resume`:
        ```
        {json_resume}
        ```
        """

    def create_prompt(self) -> str:
        return self.prompt_template.format(job_description=self.job_description,
                                           json_resume=self.json_resume)
