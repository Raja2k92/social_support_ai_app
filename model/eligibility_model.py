import os
import re

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "eligibility_model.joblib"


class EligibilityModel:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                self.train_on_synthetic()
        else:
            self.train_on_synthetic()

    # -------------------------------
    # Data preprocessing
    # -------------------------------
    def _parse_money(self, text: str) -> float:
        if not text:
            return 0.0
        matches = re.findall(r"AED\s*([\d,]+)", str(text))
        return sum(float(m.replace(",", "")) for m in matches)

    def prepare_features(self, extracted_data: dict):
        income = 0
        family = 0
        credit = 0
        net_assets = 0

        for data in extracted_data.values():
            income += data.get("Reported Monthly Income", 0)
            family += data.get("Family Members", 0)
            credit += data.get("Credit Score", 0)
            assets = self._parse_money(data.get("Assets", ""))
            liabilities = self._parse_money(data.get("Liabilities", ""))
            net_assets += max(assets - liabilities, 0)
        return np.array([[income, family, credit, net_assets]])

    # -------------------------------
    # Training on synthetic data
    # -------------------------------
    def train_on_synthetic(self):
        rng = np.random.RandomState(42)
        n = 3000

        income = rng.normal(8000, 4000, n).clip(0)
        family = rng.randint(1, 8, n)
        credit = rng.normal(650, 100, n).clip(300, 900)
        assets = rng.normal(20000, 12000, n).clip(0)
        liabilities = rng.normal(8000, 5000, n).clip(0)
        net_assets = np.maximum(assets - liabilities, 0)

        X = np.vstack([income, family, credit, net_assets]).T
        y = ((credit > 600) & (income > 5000) & (net_assets > 10000)).astype(int)

        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
        model.fit(X, y)
        self.model = model
        joblib.dump(model, MODEL_PATH)

    # -------------------------------
    # Predict
    # -------------------------------
    def predict_proba(self, applicant: dict) -> float:
        X = self.prepare_features(applicant)
        prob = float(self.model.predict_proba(X)[0, 1])

        # Calibrate into clear 0.6/0.4 bands
        if prob > 0.45:
            prob = 0.60
        else:
            prob = 0.40
        return prob
