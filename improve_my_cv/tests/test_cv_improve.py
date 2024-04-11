import json

import pytest

from improve_my_cv.cv_improve import ImproveMyCV, InvalidResponseException
from improve_my_cv.tests.mock_llm_handler import MockLLMHandler

@pytest.fixture
def valid_resume() -> str:
    valid_resume = {
        'field1': 'value1',
        'field2': 'value2',
        'date_field': '7',
        'user': 'my-email',
        'work_experience': 'this is a response'
    }
    return json.dumps(valid_resume)


def test_improve_my_cv(valid_resume: str) -> None:
    job_description = 'test_jd'
    improve = ImproveMyCV(original_resume=valid_resume, job_description=job_description)
    llm_handler = MockLLMHandler(valid_input=valid_resume)
    improved_resume = improve.improve_cv(llm_handler=llm_handler)
    assert isinstance(improved_resume, str)


def test_improve_my_cv_exception_for_invalid_input() -> None:
    invalid_input = 'This is a non json text'
    job_description = 'test_jd'
    with pytest.raises(json.decoder.JSONDecodeError):
        ImproveMyCV(original_resume=invalid_input, job_description=job_description)


def test_improve_my_cv_exception_for_invalid_llm_output(valid_resume: str) -> None:
    """Valid output of LLM should be a json string"""
    job_description = 'test_jd'
    improve = ImproveMyCV(original_resume=valid_resume, job_description=job_description)
    llm_handler = MockLLMHandler(valid_input=valid_resume, test_action='invalid_output')
    with pytest.raises(InvalidResponseException):
        improve.improve_cv(llm_handler=llm_handler)


def test_improve_my_cv_exception_for_changed_field_names(valid_resume: str) -> None:
    job_description = 'test_jd'
    improve = ImproveMyCV(original_resume=valid_resume, job_description=job_description)
    llm_handler = MockLLMHandler(valid_input=valid_resume, test_action='changed_field_names')
    with pytest.raises(InvalidResponseException):
        improve.improve_cv(llm_handler=llm_handler)


def test_improve_my_cv_exception_for_changed_dates(valid_resume: str) -> None:
    job_description = 'test_jd'
    improve = ImproveMyCV(original_resume=valid_resume, job_description=job_description)
    llm_handler = MockLLMHandler(valid_input=valid_resume, test_action='changed_dates')
    with pytest.raises(InvalidResponseException):
        improve.improve_cv(llm_handler=llm_handler)


# def test_improve_my_cv_exception_for_changed_user_data() -> None:
#     job_description = 'test_jd'
#     improve = ImproveMyCV(original_resume=valid_resume, job_description=job_description)
#     llm_handler = MockLLMHandler(valid_input=valid_resume, test_action='changed_user_data')
#     with pytest.raises(InvalidResponseException):
#         improve.improve_cv(llm_handler=llm_handler)
