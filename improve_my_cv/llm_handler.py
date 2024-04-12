import json
import requests

from abc import ABC, abstractmethod
from dataclasses import dataclass

"""We'll do it this way, to possibly check with a paid, non-local LLM"""


class LLMHandlerException(Exception):
    pass


@dataclass
class ModelResponse:
    context: list
    created_at: str
    model: str
    prompt_eval_duration_seconds: float
    total_duration_seconds: float
    text: str


class LLMHandler(ABC):
    def __init__(self, api_url: str) -> None:
        self.response = None
        self.api_url = api_url

    @abstractmethod
    def set_api_key(self, api_key: str) -> None:
        """Sets API key for the LLM"""
        pass

    @abstractmethod
    def generate(self,
                 prompt: str,
                 model: str,
                 stream: bool = False,
                 format: str = 'json') -> dict:
        """Generate content"""
        pass

    @abstractmethod
    def standardize_response(self) -> ModelResponse:
        """Convert response from specific model to the current project's format"""


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
        return ModelResponse(
            context=self.response.get('context'),
            created_at=self.response.get('created_at'),
            model=self.response.get('model'),
            prompt_eval_duration_seconds=int(self.response.get('prompt_eval_duration')) / 1e9,
            total_duration_seconds=int(self.response.get('total_duration')) / 1e9,
            text=self.response.get('response'),
        )
