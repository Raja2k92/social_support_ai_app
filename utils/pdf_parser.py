import re
from typing import Dict

from pypdf import PdfReader


def parse_pdf(file_path: str) -> Dict:
    """
    Extract structured data from a real PDF.
    Attempts to extract Name, DOB, Address, Family Members, Income, Credit Score, etc.
    """

    def extract_text(path: str) -> str:
        try:
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            return f"ERROR: {e}"

    text = extract_text(file_path)

    # Initialize output
    data = {}

    # Regex patterns for common fields
    patterns = {
        "Name": r"Name[:\s]+([A-Za-z ]+)",
        "DOB": r"DOB[:\s]+([\d/-]+)",
        "Address": r"Address[:\s]+([A-Za-z0-9, ]+)",
        "Family Members": r"Family Members[:\s]+(\d+)",
        "Reported Monthly Income": r"Monthly Income[:\s]+AED?\s*([\d,]+)",
        "Credit Score": r"Credit Score[:\s]+(\d+)",
        "Outstanding Loans": r"Outstanding Loans[:\s]+(\d+)",
        "Occupation": r"Occupation[:\s]+([A-Za-z ]+)",
        "Experience": r"Experience[:\s]+([\d ]+ years)",
        "Education": r"Education[:\s]+([A-Za-z ]+)",
        "Assets": r"Assets[:\s]+(.+)",
        "Liabilities": r"Liabilities[:\s]+(.+)",
        "Balance": r"Balance[:\s]+AED?\s*([\d,]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Convert numeric values
            if key in ["Reported Monthly Income", "Credit Score", "Outstanding Loans", "Family Members", "Balance"]:
                value = int(value.replace(",", ""))
            data[key] = value

    # Fallback: store raw text if no fields matched
    if not data:
        data["raw_text"] = text.strip() if text else "No text found"

    return data
