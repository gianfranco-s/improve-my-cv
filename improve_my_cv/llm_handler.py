import json
import requests

from abc import ABC, abstractmethod

"""We'll do it this way, to possibly check with a paid, non-local LLM"""

class LLMHandler(ABC):

    @abstractmethod
    def set_api_key(self, api_key: str) -> None:
        """Sets API key for the LLM"""
        pass

    @abstractmethod
    def generate(self) -> str:
        """Generate content"""
        pass


class HandleOllama(LLMHandler):

    def set_api_key(self) -> None:
        """Local Ollama does not require an API key"""
        pass

    def generate(self,
                 prompt: str,
                 url: str = 'http://localhost:11434/api/generate',
                 model: str = 'llama2',
                 stream: bool = False) -> dict:
        data = {
            'model': model,
            'prompt': prompt,
            'stream': stream,
        }
        response = requests.post(url=url, json=data)
        return json.loads(response.text)
