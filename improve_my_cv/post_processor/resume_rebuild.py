class ResumeRebuilder:
    """Given an original resume and a filtered_resume, update the original one to include the filtered one"""

    def __init__(self, original_resume: dict, filtered_resume: dict) -> None:
        self.original = original_resume
        self.filtered = filtered_resume

    def rebuild(self) -> dict:
        return self.filtered