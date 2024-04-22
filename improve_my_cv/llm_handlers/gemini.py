import json

import google.generativeai as genai

from datetime import datetime

from dotenv import dotenv_values
from google.ai.generativelanguage import GenerationConfig
from google.ai.generativelanguage_v1beta.types.generative_service import GenerateContentResponse

from improve_my_cv.llm_handlers.base_handler import LLMHandler, LLMHandlerException, ModelResponse


class HandleGemini(LLMHandler):
    def __init__(self, api_url: str = 'https://generativelanguage.googleapis.com') -> None:
        super().__init__(api_url=api_url)
        self.set_api_key()

    def set_api_key(self) -> None:
        """Local Ollama does not require an API key"""
        genai.configure(api_key=dotenv_values().get('GEMINI_API_KEY'))

    def generate(self,
                 prompt: str,
                 model: str = 'gemini-pro',
                 safety_settings: dict = dict()) -> GenerateContentResponse:
        generation_config = GenerationConfig({
            'candidate_count': 1,
            'temperature': 0.9,
        })        
        gemini_model = genai.GenerativeModel(model)

        try:
            responses = gemini_model.generate_content(prompt, stream=True, safety_settings=safety_settings, generation_config=generation_config)
            responses.resolve()

        except Exception as e:
            raise LLMHandlerException(e)

        self.response = responses._result

        return self.response

    def standardize_response(self) -> ModelResponse:
        try:
            response_text = self.response.candidates[0].content.parts[0].text

        except IndexError as e:
            print(e)
            print(self.response)

        return ModelResponse(
            context=self.response.prompt_feedback,
            created_at=datetime.now(),
            model='user defined',
            prompt_eval_duration_seconds=0.0,
            total_duration_seconds=0.0,
            text=response_text.replace("```json", "").replace("```", ""),
        )


if __name__ == '__main__':
    handle_model = HandleGemini()
    filepath = '/home/gsalomone/Documents/06_gian_cv/my-json-resume/src/data/base_cv.json'
    with open(filepath, 'r') as f:
        resume = json.load(f)

    response = handle_model.generate(f'Please Create a resume in json format')
    standard_resp = handle_model.standardize_response()
    print(standard_resp.text)
