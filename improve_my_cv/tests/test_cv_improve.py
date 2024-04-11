from improve_my_cv.cv_improve import ImproveMyCV

def test_cv_improve():
    improve = ImproveMyCV(r'{"field1": "value1", "field2": "value"}')
    assert isinstance(improve.improve_cv(), str)


def test_cv_improve_exception_for_invalid_input():
    pass


def test_cv_improve_exception_for_invalid_llm_output():
    pass


def test_cv_improve_exception_for_changed_field_names():
    pass


def test_cv_improve_exception_for_changed_dates():
    pass


def test_cv_improve_exception_for_changed_user_data():
    pass
