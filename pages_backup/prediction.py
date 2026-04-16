"""
pages_backup/prediction.py - Crop Yield Prediction
"""

import streamlit as st
import sys, os
import numpy as np

# ❌ REMOVED: st.set_page_config (THIS WAS BREAKING NAVBAR)

# ─────────────────────────────────────────────
# ✅ FIXED CSS (VISIBLE INPUTS + KEEP SIDEBAR)
# ─────────────────────────────────────────────
st.markdown("""
<style>

/* FORCE LIGHT MODE */
html, body, [class*="css"] {
    background-color: #f5f7f6 !important;
}

/* 🔥 FIX LABEL VISIBILITY (MAIN ISSUE) */
label, .stSelectbox label, .stNumberInput label {
    color: #000000 !important;   /* BLACK */
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* 🔥 FIX SELECTBOX TEXT */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #000000 !important;
}

/* DROPDOWN TEXT */
div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* NUMBER INPUT */
input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* INPUT BOX CONTAINER */
.stNumberInput div,
.stSelectbox div {
    background-color: #ffffff !important;
}

/* BUTTON */
button {
    background-color: #2d6a4f !important;
    color: white !important;
    border-radius: 10px !important;
    height: 45px !important;
}

/* BUTTON HOVER */
button:hover {
    background-color: #1b4332 !important;
}

/* REMOVE FADED TEXT EFFECT */
span, p {
    opacity: 1 !important;
    color: #000000 !important;
}

/* SIDEBAR FIX */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}
/* 🔥 FORCE ALL LABELS VISIBLE (NUCLEAR FIX) */
[data-testid="stWidgetLabel"] {
    color: #000000 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* ALSO TARGET INNER LABEL TEXT */
[data-testid="stWidgetLabel"] span {
    color: #000000 !important;
    opacity: 1 !important;
}

/* FIX HEADINGS FADED */
h1, h2, h3, h4, h5, h6 {
    opacity: 1 !important;
}

/* FORCE TEXT VISIBILITY EVERYWHERE */
* {
    color: inherit;
}

/* SPECIFIC FIX FOR YOUR FADED SECTION TITLES */
p, small {
    color: #333 !important;
    opacity: 1 !important;
}
            /* 🔥 FORCE FULL VISIBILITY (FINAL FIX) */
div, span, label, p, input, button {
    opacity: 1 !important;
    color: #000000 !important;
}

/* FIX INPUT TEXT */
input, textarea {
    color: #000000 !important;
    opacity: 1 !important;
}

/* FIX SELECT TEXT */
div[data-baseweb="select"] * {
    color: #000000 !important;
    opacity: 1 !important;
}

/* FIX BUTTON FADED */
button {
    opacity: 1 !important;
}

/* REMOVE ANY DISABLED LOOK */
[data-disabled="true"] {
    opacity: 1 !important;
    pointer-events: auto !important;
}
            /* 🔥 FIX LABEL TEXT (MAIN ISSUE) */
label, .stSelectbox label, .stNumberInput label {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* 🔥 FIX SECTION HEADINGS */
h2, h3, h4 {
    color: #1b4332 !important;
}

/* 🔥 FIX SMALL TEXT */
p, span {
    color: #000000 !important;
}

/* 🔥 FIX PLACEHOLDER / FADED TEXT */
input::placeholder {
    color: #555 !important;
    opacity: 1 !important;
}

/* 🔥 FORCE VISIBILITY */
* {
    opacity: 1 !important;
}
            /* 🔥 FORCE LABEL TEXT COLOR (IMPORTANT) */
div[data-testid="stWidgetLabel"] {
    color: #000000 !important;
}

/* 🔥 SELECTBOX TEXT */
div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* 🔥 INPUT TEXT (NUMBER INPUT) */
input[type="number"] {
    color: #ffffff !important;
}

/* 🔥 DROPDOWN SELECTED VALUE */
div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* 🔥 FIX FADED LABELS (THIS IS YOUR MAIN ISSUE) */
.css-1y4p8pa, .css-16idsys {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PATH FIX
# ─────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pages_backup.helpers import CROPS, SEASONS, STATES, format_yield, yield_category

# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def render():

    st.markdown("""
    <div class="page-hero">
        <h1>🌱 Yield Prediction</h1>
        <p>Enter your crop and field details to get an instant AI-powered yield forecast</p>
    </div>
    """, unsafe_allow_html=True)

    # ───────────────── MODEL LOAD ───────────────
    model_dir = os.path.join(os.path.dirname(__file__), "..", "model")
    sys.path.insert(0, model_dir)

    try:
        from preprocess import load_artifacts, encode_input

        model, le_crop, le_season, le_state = load_artifacts()
        model_loaded = True

    except Exception as e:
        st.error(f"⚠️ Model not loaded: {e}")
        return

    # ───────────────── FORM ────────────────────
    st.markdown("""
    <h2 style='color:#1b4332;'>Input Parameters</h2>
    <p>Fill in all fields for an accurate prediction</p>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        # LEFT SIDE
        with col1:
            st.markdown("### 🌾 Crop Details")

            crop = st.selectbox("Crop Type", sorted(CROPS))
            season = st.selectbox("Season", SEASONS)
            state = st.selectbox("State", sorted(STATES))
            year = st.number_input("Crop Year", min_value=1997, max_value=2030, value=2024)

        # RIGHT SIDE
        with col2:
            st.markdown("### 🌍 Field & Environmental Details")

            area = st.number_input("Area (hectares)", value=1000.0)
            rainfall = st.number_input("Annual Rainfall (mm)", value=1200.0)
            fertilizer = st.number_input("Fertilizer used (kg)", value=100000.0)
            pesticide = st.number_input("Pesticide used (kg)", value=500.0)

        submitted = st.form_submit_button("🔮 Predict Yield", use_container_width=True)

    # ───────────────── RESULT ──────────────────
    if submitted and model_loaded:
        try:
            enc_crop, enc_season, enc_state = encode_input(
                crop, season, state, le_crop, le_season, le_state
            )

            import pandas as pd

            features = pd.DataFrame([[ 
                enc_crop, year, enc_season, enc_state,
                area, rainfall, fertilizer, pesticide
            ]], columns=[
                "Crop","Crop_Year","Season","State",
                "Area","Annual_Rainfall","Fertilizer","Pesticide"
            ])

            prediction = float(model.predict(features)[0])
            label, color = yield_category(prediction)

            st.success(f"🌾 Predicted Yield: {format_yield(prediction)} ({label})")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

    # ───────────────── TIPS ────────────────────
    with st.expander("💡 Tips for Better Predictions"):
        st.markdown("""
        - Use accurate rainfall data  
        - Enter total fertilizer used  
        - Area should be in hectares  
        - Model trained on 1997–2020 data  
        """)