from improve_my_cv.prompt_creator import PromptCreator


def test_prompt_creator_create_prompt_with_valid_strings():
    prompt_template = "She's got a {job_description} reminds me {json_resume}"
    job_description = 'smile that it seems to me'
    json_resume = 'childhood memories'

    prompt_creator = PromptCreator(prompt_template=prompt_template,
                           job_description=job_description,
                           json_resume=json_resume)
    
    full_prompt = prompt_creator.create_prompt()

    assert full_prompt == prompt_template.format(job_description=job_description, json_resume=json_resume)
