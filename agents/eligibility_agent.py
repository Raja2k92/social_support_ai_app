from typing import Dict

from model.eligibility_model import EligibilityModel


class EligibilityAgent:
    def __init__(self):
        self.model = EligibilityModel()

    def assess(self, extracted_data: Dict) -> Dict:
        """Assess applicant eligibility using ML model and rule fallback."""
        try:
            prob = self.model.predict_proba(extracted_data)
            decision = "Yes" if prob >= 0.6 else "No"

            reasoning = (
                f"The machine learning model predicts a {prob:.2f} probability "
                f"of eligibility based on the applicant's income, family size, "
                f"credit score, and financial assets."
            )

            features = self.model.prepare_features(extracted_data)[0]

            return {
                "reported_income": float(features[0]),
                "family_members": int(features[1]),
                "credit_score": float(features[2]),
                "net_assets": float(features[3]),
                "eligibility_probability": round(prob, 3),
                "support": decision,
                "reasoning": reasoning,
            }

        except Exception as e:
            # Fallback to rules if data is incomplete or model error
            return self._rule_based_fallback(extracted_data, e)

    # -------------------------------
    # Simple rule-based fallback
    # -------------------------------
    def _rule_based_fallback(self, data: Dict, err=None) -> Dict:
        income = float(data.get("Reported Monthly Income", 0))
        family_members = int(data.get("Family Members", 1))
        credit_score = float(data.get("Credit Score", 0))

        assets_text = data.get("Assets", "")
        liabilities_text = data.get("Liabilities", "")

        assets = self.model._parse_money(assets_text)
        liabilities = self.model._parse_money(liabilities_text)
        liability_ratio = liabilities / (income + assets + 1)

        decision = "Yes"
        reasons = []

        if credit_score < 650:
            decision = "No"
            reasons.append("Low credit score.")
        elif income < 2500:
            decision = "No"
            reasons.append("Insufficient monthly income.")
        elif assets < 10000:
            decision = "No"
            reasons.append("Low asset value.")
        elif liability_ratio > 0.4:
            decision = "No"
            reasons.append("High liabilities compared to income and assets.")
        else:
            reasons.append("Meets baseline eligibility criteria.")

        return {
            "reported_income": income,
            "family_members": family_members,
            "credit_score": credit_score,
            "assets_value": assets,
            "liabilities_value": liabilities,
            "liability_ratio": round(liability_ratio, 2),
            "support": decision,
            "reasoning": " ".join(reasons),
            "note": f"Fallback rules applied due to model issue: {err}" if err else None,
        }
