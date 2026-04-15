"""
train_model.py
Run with: python train_model.py
"""

import pandas as pd
import numpy as np
import os
import joblib

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ── Paths ───────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "crop_yield.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)


def load_and_clean(path):
    df = pd.read_csv(path)

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    df.dropna(inplace=True)
    df = df[df["Yield"] > 0]

    return df


def train():
    print("Loading data from:", DATA_PATH)

    if not os.path.exists(DATA_PATH):
        print(f"\nERROR: CSV not found at {DATA_PATH}")
        return

    df = load_and_clean(DATA_PATH)
    print(f"Rows after cleaning: {len(df):,}")

    # ── Encoding ─────────────────────────────────────────
    le_crop   = LabelEncoder()
    le_season = LabelEncoder()
    le_state  = LabelEncoder()

    df["Crop"]   = le_crop.fit_transform(df["Crop"])
    df["Season"] = le_season.fit_transform(df["Season"])
    df["State"]  = le_state.fit_transform(df["State"])

    FEATURES = ["Crop", "Crop_Year", "Season", "State",
                "Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]

    X = df[FEATURES]
    y = df["Yield"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ── OPTIMIZED MODELS (smaller size) ─────────────────
    models = {
        "Decision Tree": DecisionTreeRegressor(max_depth=10),

        "Random Forest": RandomForestRegressor(
            n_estimators=20,        # ↓ reduced (was 200)
            max_depth=8,           # ↓ reduced
            n_jobs=-1,
            random_state=42
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=50,        # ↓ reduced (was 150)
            max_depth=3,            # ↓ reduced
            learning_rate=0.1,
            random_state=42
        ),
    }

    results = {}
    best_model, best_name, best_r2 = None, None, -np.inf

    print("\nTraining models...\n")

    for name, model in models.items():
        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        r2   = r2_score(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae  = mean_absolute_error(y_test, preds)

        results[name] = {"R2": r2, "RMSE": rmse, "MAE": mae}

        print(f"{name:20s} | R2={r2:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name

    print(f"\nBest model: {best_name} (R2={best_r2:.4f})")

    # ── SAVE (COMPRESSED) ───────────────────────────────
    joblib.dump(best_model, os.path.join(MODEL_DIR, "crop_model.pkl"), compress=3)

    joblib.dump(le_crop,   os.path.join(MODEL_DIR, "le_crop.pkl"))
    joblib.dump(le_season, os.path.join(MODEL_DIR, "le_season.pkl"))
    joblib.dump(le_state,  os.path.join(MODEL_DIR, "le_state.pkl"))

    joblib.dump(results, os.path.join(MODEL_DIR, "model_results.pkl"))

    joblib.dump({
        "best_model": best_name,
        "features": FEATURES
    }, os.path.join(MODEL_DIR, "model.pkl"))

    print("\n✅ Model saved successfully (compressed)")
    print("📦 File size reduced for GitHub compatibility")


if __name__ == "__main__":
    train()