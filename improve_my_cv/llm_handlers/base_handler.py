from abc import ABC, abstractmethod
from dataclasses import dataclass


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
