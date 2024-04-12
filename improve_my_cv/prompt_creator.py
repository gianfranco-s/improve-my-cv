from dataclasses import dataclass


@dataclass
class PromptCreator:
    job_description: str
    json_resume: str
    prompt_template: str = """
        You'll be given two parameters: `job_description` and a `json_resume`. The first one is a job description text. The latter is a resume in the JSON format.
        Please update `json_resume`'s fields to better match the `job_description`.

        Additional instructions:
        - Please only answer with an updated JSON
        - The answer should only be a JSON string
        - Do not provide any other explanation, outside the JSON response
        - Each parameter will be delimited by the characters ```

        job_description =
        ```
        {job_description}
        ```

        json_resume =
        ```
        {json_resume}
        ```
        """

    def create_prompt(self) -> str:
        return self.prompt_template.format(job_description=self.job_description,
                                           json_resume=self.json_resume)
