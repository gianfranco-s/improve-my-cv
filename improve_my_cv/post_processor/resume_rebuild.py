import copy


class ResumeRebuilder:
    def __init__(self, original_resume: dict, filtered_resume: dict) -> None:
        self.original_resume = original_resume
        self.filtered_resume = filtered_resume

    def rebuild(self) -> dict:
        rebuilt_resume = copy.deepcopy(self.original_resume)

        for section_name, section_content in self.filtered_resume.items():
            if section_name in rebuilt_resume:
                if isinstance(section_content, dict):
                    rebuilt_resume[section_name].update(section_content)
                elif isinstance(section_content, list):
                    original_items = rebuilt_resume[section_name]
                    filtered_items = section_content
                    for original_item, filtered_item in zip(original_items, filtered_items):
                        original_item.update(filtered_item)

        return rebuilt_resume
