import json

import requests

from improve_my_cv.llm_handlers.base_handler import LLMHandler, LLMHandlerException, ModelResponse


class HandleOllama(LLMHandler):
    def __init__(self, api_url: str = 'http://localhost:11434/api/generate') -> None:
        super().__init__(api_url=api_url)

    def set_api_key(self) -> None:
        """Local Ollama does not require an API key"""
        pass

    def generate(self,
                 prompt: str,
                 model: str,
                 stream: bool = False,
                 format: str = 'json') -> dict:
        data = {
            'model': model,
            'prompt': prompt,
            'stream': stream,
            'format': format,
        }
        response = requests.post(url=self.api_url, json=data)
        self.response = json.loads(response.text)

        if 'error' in self.response:
            raise LLMHandlerException(self.response)

        return self.response

    def standardize_response(self) -> ModelResponse:
        prompt_eval_duration_seconds = total_duration_seconds = -9.99
        prompt_eval_duration = self.response.get('prompt_eval_duration')
        if prompt_eval_duration:
            prompt_eval_duration_seconds = int(prompt_eval_duration) / 1e9

        total_duration = self.response.get('total_duration')
        if total_duration:
            total_duration_seconds = int(prompt_eval_duration) / 1e9

        return ModelResponse(
            context=self.response.get('context'),
            created_at=self.response.get('created_at'),
            model=self.response.get('model'),
            prompt_eval_duration_seconds=prompt_eval_duration_seconds,
            total_duration_seconds=total_duration_seconds,
            text=self.response.get('response'),
        )
