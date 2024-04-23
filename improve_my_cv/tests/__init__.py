import pytest


@pytest.fixture
def valid_resume() -> dict:
    return {
        'basics': {
            'name': 'value1',
            'label': 'value2',
            'email': '7',
        },
        'work': [
            {
                'name': 'Company 1',
                'position': 'President',
                'startDate': '2010-01-01',
            },
            {
                'name': 'NASA',
                'position': 'Astronaut',
                'startDate': '1969-01-01',
            }
        ],
    }
