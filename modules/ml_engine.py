"""
AI Career Mentor - ML Engine
Trains career prediction models and provides probability-based predictions.
Uses Random Forest + XGBoost ensemble on personality/aptitude data.
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings("ignore")

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DATA_DIR = os.path.dirname(os.path.dirname(__file__))


class CareerPredictor:
    """ML-based career prediction engine using ensemble methods."""

    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = [
            "O_score", "C_score", "E_score", "A_score", "N_score",
            "Numerical Aptitude", "Spatial Aptitude", "Perceptual Aptitude",
            "Abstract Reasoning", "Verbal Reasoning"
        ]
        self.is_trained = False
        self._load_or_train()

    def _load_or_train(self):
        """Load saved model or train new one."""
        model_path = os.path.join(MODEL_DIR, "career_model.pkl")
        scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
        encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")

        if all(os.path.exists(p) for p in [model_path, scaler_path, encoder_path]):
            try:
                with open(model_path, "rb") as f:
                    self.model = pickle.load(f)
                with open(scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
                with open(encoder_path, "rb") as f:
                    self.label_encoder = pickle.load(f)
                self.is_trained = True
                return
            except Exception:
                pass

        self._train_model()

    def _augment_data(self, df, n_augmented=20):
        """Augment small dataset with synthetic variations."""
        augmented_rows = []
        for _, row in df.iterrows():
            for _ in range(n_augmented):
                new_row = row.copy()
                for col in self.feature_names:
                    noise = np.random.normal(0, 0.3)
                    new_row[col] = np.clip(new_row[col] + noise, 1, 10)
                augmented_rows.append(new_row)
        augmented_df = pd.DataFrame(augmented_rows)
        return pd.concat([df, augmented_df], ignore_index=True)

    def _train_model(self):
        """Train ensemble model on career dataset."""
        data_path = os.path.join(DATA_DIR, "Data_final.csv")
        if not os.path.exists(data_path):
            return

        df = pd.read_csv(data_path)
        df = self._augment_data(df, n_augmented=25)

        X = df[self.feature_names].values
        y = self.label_encoder.fit_transform(df["Career"].values)

        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        rf = RandomForestClassifier(
            n_estimators=300, max_depth=15, min_samples_split=3,
            min_samples_leaf=2, random_state=42, class_weight="balanced"
        )
        gb = GradientBoostingClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.1,
            min_samples_split=3, random_state=42
        )

        self.model = VotingClassifier(
            estimators=[("rf", rf), ("gb", gb)],
            voting="soft", weights=[1, 1]
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        self.is_trained = True

        os.makedirs(MODEL_DIR, exist_ok=True)
        with open(os.path.join(MODEL_DIR, "career_model.pkl"), "wb") as f:
            pickle.dump(self.model, f)
        with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
            pickle.dump(self.scaler, f)
        with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
            pickle.dump(self.label_encoder, f)

    def predict_career(self, scores: dict) -> list:
        """
        Predict career probabilities from assessment scores.
        Returns list of (career, probability) sorted by probability descending.
        """
        if not self.is_trained:
            return []

        features = np.array([[scores.get(f, 5.0) for f in self.feature_names]])
        features_scaled = self.scaler.transform(features)

        probabilities = self.model.predict_proba(features_scaled)[0]
        careers = self.label_encoder.classes_

        results = sorted(
            zip(careers, probabilities),
            key=lambda x: x[1],
            reverse=True
        )
        return results

    def get_top_careers(self, scores: dict, top_n: int = 8) -> list:
        """Get top N career predictions with percentages."""
        all_predictions = self.predict_career(scores)
        top = all_predictions[:top_n]
        # Normalize top predictions to sum closer to meaningful %
        total = sum(p for _, p in top)
        if total > 0:
            return [(career, round((prob / total) * 100, 1)) for career, prob in top]
        return top

    def get_model_accuracy(self) -> float:
        """Return model accuracy."""
        return getattr(self, "accuracy", 0.0)

    def get_career_classes(self) -> list:
        """Return all career classes."""
        if self.is_trained:
            return list(self.label_encoder.classes_)
        return []
