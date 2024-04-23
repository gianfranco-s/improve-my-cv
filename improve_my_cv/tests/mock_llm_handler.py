import copy
import json

from improve_my_cv.llm_handlers.base_handler import LLMHandler, ModelResponse


class MockLLMHandler(LLMHandler):

    def __init__(self,
                 valid_input_resume: dict,
                 test_action: str = 'valid_output') -> None:
        self.valid_input_resume = valid_input_resume
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


def test_action(action: str, valid_input: dict) -> str:

    output = {
        'valid_output': _generate_valid_output(valid_input),
        'invalid_output': 'This is a non json text',
        'changed_field_names': _generate_output_with_changed_field_names(valid_input),
    }

    if action not in output.keys():
        raise ValueError(f'Invalid test action {action}')

    return json.dumps(output.get(action))


def _generate_valid_output(valid_input: dict) -> dict:
    """Hardcoded based on current values of `valid_resume`"""
    updated_output = copy.deepcopy(valid_input)
    updated_output['basics'].update({'label': 'value2_new'})
    updated_output['work'][0].update({'position': 'President_new'})
    updated_output['work'][1].update({'position': 'Astronaut_new'})
    return updated_output


def _generate_output_with_changed_field_names(valid_input: dict) -> dict:
    """Hardcoded based on current values of `valid_resume`"""
    updated_output = copy.deepcopy(valid_input)
    updated_output['basics']['label_new'] = updated_output['basics'].pop('label')
    for item in updated_output['work']:
        item['position_new'] = item.pop('position')
    return updated_output
