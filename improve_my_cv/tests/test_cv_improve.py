import json

import pytest

from improve_my_cv.cv_improve import ImproveMyCV, InvalidResponseException
from improve_my_cv.llm_handler import LLMHandler


class MockLLMHandler(LLMHandler):
    valid_input = '{"field1": "value1", "field2": "value2", "date_field" = "7", "user": "my-email"}'

    def __init__(self, valid_input: str = valid_input,
                 test_action: str = 'valid_input') -> None:
        self.valid_input = valid_input
        self.test_action = test_action

    def set_api_key(self) -> None:
        pass

    def generate(self) -> str:
        valid_input = json.loads(self.valid_input)

        actions = {
            'valid_output': {key: f'{val}_new' for key, val in valid_input.items()},
            'invalid_output': 'This is a non json text',
            'changed_field_names': {f'{key}_new': val for key, val in valid_input.items()},
            'changed_dates': {key: f'{val}_new' for key, val in valid_input.items() if 'date' in key},
            'changed_user_data': {key: f'{val}_new' for key, val in valid_input.items() if 'user' in key},
        }

        if self.test_action not in actions:
            raise ValueError(f'Invalid action {self.test_action}')

        return json.dumps(actions.get(self.test_action))


def test_improve_my_cv() -> None:
    original_resume = r'{"field1": "value1", "field2": "value"}'
    improve = ImproveMyCV(original_resume=original_resume)
    assert isinstance(improve.improve_cv(), str)


def test_improve_my_cv_exception_for_invalid_input() -> None:
    invalid_input = 'This is a non json text'
    with pytest.raises(Exception):
        ImproveMyCV(original_resume=invalid_input)


def test_improve_my_cv_exception_for_invalid_llm_output() -> None:
    original_resume = r'{"field1": "value1", "field2": "value"}'
    improve = ImproveMyCV(original_resume=original_resume)

    with pytest.raises(json.JSONDecodeError):
        improve.improve_cv(prompt='test prompt', llm_handler=MockLLMHandler(test_action='invalid_output'))


def test_improve_my_cv_exception_for_changed_field_names() -> None:
    original_resume = r'{"field1": "value1", "field2": "value"}'
    improve = ImproveMyCV(original_resume=original_resume)

    with pytest.raises(InvalidResponseException):
        improve.improve_cv(prompt='test prompt', llm_handler=MockLLMHandler(test_action='changed_field_names'))


def test_improve_my_cv_exception_for_changed_dates() -> None:
    original_resume = r'{"field1": "value1", "field2": "value"}'
    improve = ImproveMyCV(original_resume=original_resume)

    with pytest.raises(InvalidResponseException):
        improve.improve_cv(prompt='test prompt', llm_handler=MockLLMHandler(test_action='changed_dates'))


def test_improve_my_cv_exception_for_changed_user_data() -> None:
    original_resume = r'{"field1": "value1", "field2": "value"}'
    improve = ImproveMyCV(original_resume=original_resume)

    with pytest.raises(InvalidResponseException):
        improve.improve_cv(prompt='test prompt', llm_handler=MockLLMHandler(test_action='changed_user_data'))
