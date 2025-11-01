from typing import Dict, List

from mock_db.mongo_mock import mongo_mock
from mock_db.vector_mock import vector_mock
from utils.pdf_parser import parse_pdf


class DataExtractionAgent:
    def process(self, attachments: List[str]) -> Dict:
        extracted_data = {}
        for file_path in attachments:
            data = parse_pdf(file_path)
            extracted_data[file_path] = data

        # Save DB
        mongo_mock(extracted_data)
        vector_mock(attachments)

        return extracted_data
