import json

default_allowed_resume_values = {
    'basics': ('label', 'summary'),
    'work': ('position', 'summary', 'highlights'),
    'volunteer': ('position', 'summary'),
    'publications': ('summary', ),
    'skills': ('name', 'keywords'),
    'interests': ('name', 'keywords'),
    'projects': ('description', 'highlights'),
}


def _extract_fields(resume: dict, allowed_sections: tuple) -> dict:
    extracted_resume = dict()

    for section in allowed_sections:
        extracted_resume[section] = resume[section]
    
    return extracted_resume


def filter_resume(resume: str, allowed_sections: dict = default_allowed_resume_values) -> dict:
    """Filters by allowed_sections, to avoid having the LLM changing unwanted fields.
    resume should be JSON-like"""
    resume = json.loads(resume)

    ext_fields = dict()

    for section, subsections in allowed_sections.items():
        resume_section = resume[section]
        if resume_section is None:
            continue
        if not isinstance(resume_section, list):
            ext_fields.update({section: _extract_fields(resume_section, subsections)})
        else:
            array_items = []
            for item in resume_section:
                filtered_item = _extract_fields(item, subsections)
                array_items.append(filtered_item)
            ext_fields.update({section: array_items})
    
    return ext_fields


if __name__ == '__main__':
    with open('/home/gsalomone/Documents/06_gian_cv/my-json-resume/src/data/base_cv.json', 'r') as f:
        resume = json.load(f)
    
    ext_resume = filter_resume(resume)

    with open('extracted_resume.json', 'w') as f:
        json.dump(ext_resume, f, indent=4)
