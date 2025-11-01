from typing import Dict, List

from utils.pdf_parser import parse_pdf


class DataExtractionAgent:
    def process(self, attachments: List[str]) -> Dict:
        extracted_data = {}
        for file_path in attachments:
            data = parse_pdf(file_path)
            extracted_data[file_path] = data

        return extracted_data
