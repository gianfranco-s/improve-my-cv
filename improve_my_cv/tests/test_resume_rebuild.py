from deepdiff import DeepDiff

from improve_my_cv.post_processor.resume_rebuild import ResumeRebuilder


def test_resume_rebuilder() -> None:
    original = {
        'basics': {
            'name': 'nameval',
            'email': 'emailval',
            'label': 'label orig',
        },
        'work': [
            {
                'name': 'work1',
                'summary': 'summary orig 1'
            },
            {
                'name': 'work2',
                'summary': 'summary orig 2'
            },
        ]
    }

    improved = {
        'basics': {
            'label': 'label new',
        },
        'work': [
            {
                'summary': 'summary new 1'
            },
            {
                'summary': 'summary new 2'
            },
        ]
    }

    expected_result = {
        'basics': {
            'name': 'nameval',
            'email': 'emailval',
            'label': 'label new',
        },
        'work': [
            {
                'name': 'work1',
                'summary': 'summary new 1'
            },
            {
                'name': 'work2',
                'summary': 'summary new 2'
            },
        ]
    }

    rebuilder = ResumeRebuilder(original_resume=original, filtered_resume=improved)
    rebuilt_resume = rebuilder.rebuild()

    diff = DeepDiff(rebuilt_resume, expected_result)

    assert len(diff) == 0
