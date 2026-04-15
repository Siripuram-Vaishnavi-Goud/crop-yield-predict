"""pages/home.py — Landing page"""

import streamlit as st


def render():
    # ── Hero ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-hero">
        <h1>🌾 CropSight</h1>
        <p>AI-powered crop yield prediction for smarter agricultural decisions across India</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Crop Varieties", "55", help="Unique crops in dataset")
    with c2:
        st.metric("States Covered", "30", help="Indian states & UTs")
    with c3:
        st.metric("Years of Data", "24", "1997 – 2020")
    with c4:
        st.metric("Model Accuracy", "90.8%", "R² score")

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Feature cards ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-title">What CropSight Offers</div>
    <div class="section-sub">Everything you need to make data-driven farming decisions</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div style="font-size:2rem;">📊</div>
            <b>Dashboard</b>
            <p>Visual overview of crop trends and performance.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div style="font-size:2rem;">🌱</div>
            <b>Yield Prediction</b>
            <p>Instant AI-based crop yield prediction.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div style="font-size:2rem;">💡</div>
            <b>Recommendations</b>
            <p>Best crops based on historical data.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── CTA ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="card-green" style="text-align:center; padding: 2rem;">
        <b>Ready to predict your crop yield?</b>
        <p>Go to prediction page from sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("🌱 Try Prediction", use_container_width=True):
            st.session_state.page = "prediction"
            st.rerun()