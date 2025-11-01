from typing import Dict, List, TypedDict


class AppState(TypedDict, total=False):
    attachments: List[str]
    extracted_data: Dict
    validation: Dict
    eligibility: Dict
    decision: Dict
