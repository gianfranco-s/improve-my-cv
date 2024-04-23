import pytest

from improve_my_cv.cv_improve import ImproveMyCV, InvalidResponseException, InvalidResumeInputException
from improve_my_cv.tests.mock_llm_handler import MockLLMHandler
from improve_my_cv.tests import valid_resume


@pytest.fixture
def test_job_description() -> str:
    return 'test jd'


def test_improve_my_cv(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume)
    improve.llm_setup(model='mock-model', llm_handler=llm_handler)
    improved_resume = improve.improve_cv()
    assert isinstance(improved_resume, dict)


def test_improve_my_cv_exception_for_invalid_input(test_job_description: str) -> None:
    invalid_input = 'This is a non json text'
    with pytest.raises(InvalidResumeInputException):
        ImproveMyCV(original_resume=invalid_input, job_description=test_job_description)


def test_improve_my_cv_exception_for_invalid_llm_output(valid_resume: dict, test_job_description: str) -> None:
    """Valid output of LLM should be a json-like string"""
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='invalid_output')
    improve.llm_setup(model='mock-model', llm_handler=llm_handler)
    with pytest.raises(InvalidResponseException):
        improve.improve_cv()


def test_improve_my_cv_warning_for_changed_field_names(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='changed_field_names')
    improve.llm_setup(model='mock-model', llm_handler=llm_handler)
    improve.improve_cv()
    new_field_names = improve.response_warnings().get('field_names_changed') - set(valid_resume.keys())
    assert all([field.endswith('_new') for field in new_field_names])
