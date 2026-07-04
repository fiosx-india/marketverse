"""
=========================================================
MarketVerse AI - Machine Learning Engine
=========================================================

Trains and predicts market direction using
Random Forest Classifier.

Future Ready:
- XGBoost
- LightGBM
- LSTM
- Deep Learning

=========================================================
"""

import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


MODEL_FILE = "marketverse_model.pkl"


class AIModel:

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42
        )

    ####################################################
    # Train Model
    ####################################################

    def train(self, df):

        if df is None or len(df) < 50:
            return {
                "success": False,
                "accuracy": 0
            }

        data = df.copy()

        data["Target"] = (
            data["Close"].shift(-1) > data["Close"]
        ).astype(int)

        data = data.dropna()

        features = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        X = data[features]
        y = data["Target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        prediction = self.model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            prediction
        )

        return {
            "success": True,
            "accuracy": round(accuracy * 100, 2)
        }

    ####################################################
    # Predict
    ####################################################

    def predict(self, latest_row):

        prediction = self.model.predict(latest_row)[0]

        probability = self.model.predict_proba(
            latest_row
        )[0]

        confidence = max(probability) * 100

        signal = "BUY"

        if prediction == 0:
            signal = "SELL"

        return {
            "signal": signal,
            "confidence": round(confidence, 2)
        }

    ####################################################
    # Save
    ####################################################

    def save(self):

        joblib.dump(
            self.model,
            MODEL_FILE
        )

    ####################################################
    # Load
    ####################################################

    def load(self):

        if os.path.exists(MODEL_FILE):

            self.model = joblib.load(
                MODEL_FILE
            )

            return True

        return False

    ####################################################
    # Feature Importance
    ####################################################

    def feature_importance(self):

        names = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        importance = self.model.feature_importances_

        return dict(
            zip(names, importance)
        )


########################################################
# Helper Function
########################################################

def train_ai(df):

    model = AIModel()

    result = model.train(df)

    if result["success"]:
        model.save()

    return result


def predict_ai(df):

    model = AIModel()

    model.load()

    latest = df[[
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]].tail(1)

    return model.predict(latest)


############################################################
# Future Models
############################################################

def train_xgboost(df):
    """
    Placeholder for future XGBoost implementation.
    """
    return {
        "success": False,
        "message": "XGBoost training not implemented yet."
    }


def train_lstm(df):
    """
    Placeholder for future LSTM implementation.
    """
    return {
        "success": False,
        "message": "LSTM training not implemented yet."
    }


def predict_with_saved_model(df):
    """
    Predict using saved Random Forest model.
    """

    model = AIModel()

    if not model.load():
        return {
            "signal": "HOLD",
            "confidence": 0,
            "error": "Model not trained"
        }

    latest = df[
        [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]
    ].tail(1)

    return model.predict(latest)
