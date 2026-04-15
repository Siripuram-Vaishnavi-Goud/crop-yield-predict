<<<<<<< HEAD
"""
preprocess.py — shared preprocessing helpers for inference
"""

import pickle
import os
import numpy as np

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))


def _load(fname):
    path = os.path.join(MODEL_DIR, fname)
    with open(path, "rb") as f:
        return pickle.load(f)


def load_artifacts():
    """Return (model, le_crop, le_season, le_state)."""
    model     = _load("crop_model.pkl")
    le_crop   = _load("le_crop.pkl")
    le_season = _load("le_season.pkl")
    le_state  = _load("le_state.pkl")
    return model, le_crop, le_season, le_state


def encode_input(crop, season, state, le_crop, le_season, le_state):
    """Safely label-encode inputs; raise ValueError for unknowns."""
    def safe_encode(le, val, name):
        if val not in le.classes_:
            raise ValueError(f"Unknown {name}: '{val}'")
        return le.transform([val])[0]

    return (
        safe_encode(le_crop,   crop,   "Crop"),
        safe_encode(le_season, season, "Season"),
        safe_encode(le_state,  state,  "State"),
    )


def predict_yield(crop, crop_year, season, state,
                  area, rainfall, fertilizer, pesticide):
    """Run full prediction pipeline. Returns float yield value."""
    import pandas as pd
    model, le_crop, le_season, le_state = load_artifacts()

    enc_crop, enc_season, enc_state = encode_input(
        crop, season, state, le_crop, le_season, le_state
    )

    features = pd.DataFrame([[
        enc_crop, crop_year, enc_season, enc_state,
        area, rainfall, fertilizer, pesticide
    ]], columns=["Crop","Crop_Year","Season","State",
                 "Area","Annual_Rainfall","Fertilizer","Pesticide"])

    return float(model.predict(features)[0])


def get_label_classes():
    """Return dicts of original class names for UI dropdowns."""
    le_crop   = _load("le_crop.pkl")
    le_season = _load("le_season.pkl")
    le_state  = _load("le_state.pkl")
    return {
        "crops":   sorted(le_crop.classes_.tolist()),
        "seasons": sorted(le_season.classes_.tolist()),
        "states":  sorted(le_state.classes_.tolist()),
=======
"""
preprocess.py — shared preprocessing helpers for inference
"""

import pickle
import os
import numpy as np

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))


def _load(fname):
    path = os.path.join(MODEL_DIR, fname)
    with open(path, "rb") as f:
        return pickle.load(f)


def load_artifacts():
    """Return (model, le_crop, le_season, le_state)."""
    model     = _load("crop_model.pkl")
    le_crop   = _load("le_crop.pkl")
    le_season = _load("le_season.pkl")
    le_state  = _load("le_state.pkl")
    return model, le_crop, le_season, le_state


def encode_input(crop, season, state, le_crop, le_season, le_state):
    """Safely label-encode inputs; raise ValueError for unknowns."""
    def safe_encode(le, val, name):
        if val not in le.classes_:
            raise ValueError(f"Unknown {name}: '{val}'")
        return le.transform([val])[0]

    return (
        safe_encode(le_crop,   crop,   "Crop"),
        safe_encode(le_season, season, "Season"),
        safe_encode(le_state,  state,  "State"),
    )


def predict_yield(crop, crop_year, season, state,
                  area, rainfall, fertilizer, pesticide):
    """Run full prediction pipeline. Returns float yield value."""
    import pandas as pd
    model, le_crop, le_season, le_state = load_artifacts()

    enc_crop, enc_season, enc_state = encode_input(
        crop, season, state, le_crop, le_season, le_state
    )

    features = pd.DataFrame([[
        enc_crop, crop_year, enc_season, enc_state,
        area, rainfall, fertilizer, pesticide
    ]], columns=["Crop","Crop_Year","Season","State",
                 "Area","Annual_Rainfall","Fertilizer","Pesticide"])

    return float(model.predict(features)[0])


def get_label_classes():
    """Return dicts of original class names for UI dropdowns."""
    le_crop   = _load("le_crop.pkl")
    le_season = _load("le_season.pkl")
    le_state  = _load("le_state.pkl")
    return {
        "crops":   sorted(le_crop.classes_.tolist()),
        "seasons": sorted(le_season.classes_.tolist()),
        "states":  sorted(le_state.classes_.tolist()),
>>>>>>> d0e113e (Added project with model files)
    }