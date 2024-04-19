import json

import pytest

from improve_my_cv.cv_improve import ImproveMyCV, InvalidResponseException, InvalidResumeInputException
from improve_my_cv.tests.mock_llm_handler import MockLLMHandler


@pytest.fixture
def valid_resume() -> dict:
    return {
        'field1': 'value1',
        'field2': 'value2',
        'date_field': '7',
        'name': 'username',
        'work_experience': 'this is a response'
    }


@pytest.fixture
def test_job_description() -> str:
    return 'test jd'


def test_improve_my_cv(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume)
    improved_resume = improve.improve_cv(llm_handler=llm_handler)
    assert isinstance(improved_resume, dict)


def test_improve_my_cv_exception_for_invalid_input(test_job_description: str) -> None:
    invalid_input = 'This is a non json text'
    with pytest.raises(InvalidResumeInputException):
        ImproveMyCV(original_resume=invalid_input, job_description=test_job_description)


def test_improve_my_cv_exception_for_invalid_llm_output(valid_resume: dict, test_job_description: str) -> None:
    """Valid output of LLM should be a json-like string"""
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='invalid_output')
    with pytest.raises(InvalidResponseException):
        improve.improve_cv(llm_handler=llm_handler)


def test_improve_my_cv_warning_for_changed_field_names(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='changed_field_names')
    improve.improve_cv(llm_handler=llm_handler)
    new_field_names = improve.response_warnings().get('field_names_changed') - set(valid_resume.keys())
    assert all([field.endswith('_new') for field in new_field_names])


def test_improve_my_cv_warning_for_changed_dates(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='changed_dates')
    improve.improve_cv(llm_handler=llm_handler)
    dates_changed = improve.response_warnings().get('dates_changed').get('date_field')
    org_date, new_date = dates_changed.split(' -> ')
    assert org_date == valid_resume.get('date_field')
    assert new_date == valid_resume.get('date_field') + '_new'


def test_improve_my_cv_warning_for_changed_user_data(valid_resume: dict, test_job_description: str) -> None:
    improve = ImproveMyCV(original_resume=valid_resume, job_description=test_job_description)
    llm_handler = MockLLMHandler(valid_input_resume=valid_resume, test_action='changed_user_data')
    improve.improve_cv(llm_handler=llm_handler)
    assert improve.response_warnings().get('is_user_data_changed') is True
