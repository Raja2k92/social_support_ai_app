from typing import Dict

from utils.llm_client import ask_ollama


class DecisionAgent:
    def make_decision(self, validated_data: Dict, eligibility: Dict, extracted_data: Dict) -> Dict:
        """
        Uses LLM (Ollama local model) to generate:
          1. Financial support recommendation
          2. Economic enablement suggestions
        Considers 'support': 'Yes' in eligibility to bias the decision positively.
        """

        # Extract key applicant information dynamically
        applicant_info = {
            "Name": None,
            "Occupation": None,
            "Experience": None,
            "Education": None,
            "Reported Monthly Income": None,
            "Address": None,
            "Family Members": None
        }

        for _, data in extracted_data.items():
            for key in applicant_info.keys():
                if key in data and not applicant_info[key]:
                    applicant_info[key] = data[key]

        # Interpret eligibility decision
        support_flag = eligibility.get("support", "").strip().lower() == "yes"
        eligibility_status = "Eligible for social support" if support_flag else "Not eligible for social support"

        # Construct the LLM prompt
        prompt = f"""
You are an AI decision support officer assessing a social welfare application.

Applicant Summary:
Name: {applicant_info.get('Name')}
Occupation: {applicant_info.get('Occupation')}
Experience: {applicant_info.get('Experience')}
Education: {applicant_info.get('Education')}
Monthly Income: {applicant_info.get('Reported Monthly Income')}
Family Members: {applicant_info.get('Family Members')}
Address: {applicant_info.get('Address')}

Validation Results:
{validated_data}

Eligibility:
{eligibility_status}

Decision Logic:
- If 'support' is Yes, likely approve the financial support unless serious validation issues.
- If 'support' is No or uncertain, recommend a soft decline with justification.
- Always provide economic enablement support suggestions regardless of decision.

Respond in valid JSON format:
{{
  "financial_support_decision": "Approve" or "Decline",
  "reasoning": "soft short justification",
  "economic_enablement_suggestions": ["...", "..."]
}}
"""

        # Call local LLM (Gemma via Ollama)
        decision_response = ask_ollama(prompt)

        return {"recommendation": decision_response}
