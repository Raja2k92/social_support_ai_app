from typing import Dict


def validate_applicant_data(extracted_data: Dict) -> Dict:
    """
    Dynamically validates applicant data across PDFs without hardcoding filenames.
    Returns:
      - income_check: True if any PDF has 'Reported Monthly Income' > 0
      - family_check: True if any PDF has 'Family Members' > 0
      - address_check: True if at least two PDFs have 'Address' and they match
    """

    validation = {
        "income_check": False,
        "family_check": False,
        "address_check": False
    }

    # --- Income check ---
    for pdf_data in extracted_data.values():
        income = pdf_data.get("Reported Monthly Income")
        if isinstance(income, int) and income > 0:
            validation["income_check"] = True
            break

    # --- Family members check ---
    for pdf_data in extracted_data.values():
        family = pdf_data.get("Family Members")
        if isinstance(family, int) and family > 0:
            validation["family_check"] = True
            break

    # --- Address check ---
    # Collect all addresses
    addresses = [pdf_data.get("Address") for pdf_data in extracted_data.values() if pdf_data.get("Address")]
    # If there are at least two addresses, check if all match
    if len(addresses) >= 2:
        first_address = addresses[0].strip().lower()
        validation["address_check"] = all(addr.strip().lower() == first_address for addr in addresses[1:])

    return validation
