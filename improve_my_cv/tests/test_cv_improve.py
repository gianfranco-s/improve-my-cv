import pytest

from improve_my_cv.cv_improve import ImproveMyCV
from improve_my_cv.llm_handler import LLMHandler

class MockLLMHandler(LLMHandler):
    def __init__(self, test_action: str = 'valid_input') -> None:
        self.test_action = test_action

    def set_api_key(self) -> None:
        pass

    def generate(self) -> str:
        # valid_input = r'{"field1": "value1", "field2": "value2"}'
        valid_output = r'{"field1": "value3", "field2": "value4"}'
        
        actions = {
            'valid_output': valid_output,
            'invalid_output': 'This is a non json text',
        }

        if self.test_action not in actions:
            raise ValueError(f'Invalid action {self.test_action}')

        return actions.get(self.test_action)


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

    with pytest.raises(Exception):
        improve.improve_cv(prompt='test prompt', llm_handler=MockLLMHandler(test_action='invalid_output'))


def test_improve_my_cv_exception_for_changed_field_names() -> None:
    pass


def test_improve_my_cv_exception_for_changed_dates() -> None:
    pass


def test_improve_my_cv_exception_for_changed_user_data() -> None:
    pass
