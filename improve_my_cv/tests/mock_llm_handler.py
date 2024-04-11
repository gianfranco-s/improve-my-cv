import json

from improve_my_cv.llm_handler import LLMHandler, ModelResponse


class MockLLMHandler(LLMHandler):

    def __init__(self, 
                 valid_input: str,
                 test_action: str = 'valid_output') -> None:
        self.valid_input_resume = valid_input
        self.test_action = test_action
        self.response = None

    def set_api_key(self) -> None:
        pass

    def generate(self, prompt: str, model: str) -> dict:
        """It's expected that the model will return a `model_generated_response`
        The fields of this dictionary depend on the specific LLM used
        """
        
        model_generated_response = {
            'context': None,
            'created_at': None,
            'model': None,
            'prompt_eval_duration': None,
            'total_duration': None,
            'response': test_action(self.test_action, self.valid_input_resume),
        }

        self.response = model_generated_response
        return self.response

    def standardize_response(self) -> ModelResponse:
        return ModelResponse(
            context=None,
            created_at=None,
            model=None,
            prompt_eval_duration_seconds=None,
            total_duration_seconds=None,
            text=self.response.get('response'),
        )


def test_action(action: str, valid_input: str):
    input = json.loads(valid_input)

    output = {
        'valid_output': {key: f'{val}_new' for key, val in input.items()},
        'invalid_output': 'This is a non json text',
        'changed_field_names': {f'{key}_new': val for key, val in input.items()},
        'changed_dates': {key: f'{val}_new' for key, val in input.items() if 'date' in key},
        'changed_user_data': {key: f'{val}_new' for key, val in input.items() if 'user' in key},
    }

    if action not in output.keys():
        raise ValueError(f'Invalid test action {action}')
    
    return output.get(action)
