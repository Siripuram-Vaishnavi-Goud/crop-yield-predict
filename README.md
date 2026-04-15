# 🌾 CropSight — Crop Yield Prediction Platform

AI-powered crop yield prediction for smarter agricultural decisions across India.

## 📁 Project Structure

```
crop_project/
├── app.py                   # Main Streamlit entry point
├── style.css                # Global theme (clean agricultural)
├── requirements.txt
├── users.db                 # Auto-created SQLite auth DB
├── dataset/
│   └── crop_yield.csv
├── model/
│   ├── train_model.py       # Train & compare models, save best
│   ├── preprocess.py        # Encoding & inference helpers
│   ├── crop_model.pkl       # Best trained model
│   ├── le_crop.pkl
│   ├── le_season.pkl
│   ├── le_state.pkl
│   ├── model.pkl
│   ├── model_results.pkl    # All model comparison results
│   └── feature_importances.pkl
├── pages/
│   ├── home.py              # Landing page
│   ├── login.py             # Auth — login
│   ├── register.py          # Auth — register
│   ├── dashboard.py         # Analytics dashboard (login required)
│   ├── dataset_analysis.py  # Interactive data exploration
│   ├── prediction.py        # Yield prediction form
│   ├── recommendation.py    # Best crop recommendations
│   └── contact.py
└── utils/
    ├── auth.py              # SQLite auth helpers
    └── helpers.py           # Shared data loading & constants
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train the model (first time only)
python model/train_model.py

# 3. Run the app
streamlit run app.py
```

## 🤖 Model Performance

| Model              | R²     | RMSE    | MAE     |
|--------------------|--------|---------|---------|
| Decision Tree      | 0.8741 | 289.29  | 11.67   |
| **Random Forest**  | **0.9078** | **247.58** | **11.01** |
| Gradient Boosting  | 0.9002 | 257.51  | 12.89   |

**Random Forest selected** as best model (R²=0.9078).

## 📊 Dataset

- **Source**: Indian Agricultural Statistics (ICAR)
- **Records**: 19,577 (after cleaning)
- **Coverage**: 55 crops · 30 states · 1997–2020
- **Features**: Crop, Season, State, Area, Annual Rainfall, Fertilizer, Pesticide → **Yield**

## 🔐 Authentication

- Dashboard page requires login
- Passwords hashed with SHA-256
- SQLite DB auto-created at first run

## 📄 Pages

| Page | Auth Required | Description |
|------|--------------|-------------|
| Home | No | Overview & feature cards |
| Dashboard | ✅ Yes | Charts, trends, correlations |
| Dataset Analysis | No | Interactive data exploration |
| Prediction | No | Yield prediction form |
| Recommendation | No | Best crops by state/season |
| Contact | No | Contact form |