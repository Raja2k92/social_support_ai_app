from typing import Dict

from utils.validation_utils import validate_applicant_data


class DataValidationAgent:
    def process(self, extracted_data: Dict) -> Dict:
        validation_result = {}
        validation_result = validate_applicant_data(extracted_data)

        return validation_result
