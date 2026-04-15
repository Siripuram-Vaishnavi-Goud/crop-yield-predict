"""
train_model.py  (ROOT FILE — place this at CropYieldPrediction/train_model.py)
Run with:  python train_model.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ── Paths (works from any working directory) ───────────────────────────────
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
        print("Please create a 'dataset' folder and put crop_yield.csv inside it.")
        return

    df = load_and_clean(DATA_PATH)
    print(f"Rows after cleaning: {len(df):,}")

    # Encode categorical columns
    le_crop   = LabelEncoder()
    le_season = LabelEncoder()
    le_state  = LabelEncoder()

    df["Crop"]   = le_crop.fit_transform(df["Crop"])
    df["Season"] = le_season.fit_transform(df["Season"])
    df["State"]  = le_state.fit_transform(df["State"])

    FEATURES = ["Crop", "Crop_Year", "Season", "State",
                "Area", "Annual_Rainfall", "Fertilizer", "Pesticide"]
    TARGET   = "Yield"

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ── Train 3 models and compare ─────────────────────────────────────────
    models = {
        "Decision Tree": DecisionTreeRegressor(
            max_depth=12, min_samples_split=5,
            min_samples_leaf=3, random_state=42
        ),
        "Random Forest": RandomForestRegressor(
            n_estimators=200, max_depth=15,
            min_samples_split=4, min_samples_leaf=2,
            n_jobs=-1, random_state=42
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=150, learning_rate=0.1,
            max_depth=6, random_state=42
        ),
    }

    results = {}
    best_name, best_model, best_r2 = None, None, -np.inf

    print("\nTraining models...\n")
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        r2   = r2_score(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae  = mean_absolute_error(y_test, preds)
        results[name] = {"R2": r2, "RMSE": rmse, "MAE": mae}
        print(f"  {name:25s} | R2={r2:.4f} | RMSE={rmse:.4f} | MAE={mae:.4f}")
        if r2 > best_r2:
            best_r2, best_name, best_model = r2, name, model

    print(f"\nBest model: {best_name} (R2={best_r2:.4f})")

    # ── Save all files into model/ folder ──────────────────────────────────
    def save(obj, filename):
        with open(os.path.join(MODEL_DIR, filename), "wb") as f:
            pickle.dump(obj, f)

    save(best_model, "crop_model.pkl")
    save(le_crop,    "le_crop.pkl")
    save(le_season,  "le_season.pkl")
    save(le_state,   "le_state.pkl")
    save(results,    "model_results.pkl")
    save({"best": best_name, "features": FEATURES}, "model.pkl")

    # Feature importances
    if hasattr(best_model, "feature_importances_"):
        fi = dict(zip(FEATURES, best_model.feature_importances_))
        save(dict(sorted(fi.items(), key=lambda x: x[1], reverse=True)),
             "feature_importances.pkl")

    print("\nAll .pkl files saved to model/ folder")
    print("Done! You can now run:  streamlit run app.py")


if __name__ == "__main__":
    train()