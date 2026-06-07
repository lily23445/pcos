# PCOS Tracker

A Streamlit-based personal health dashboard designed to help track PCOS symptoms, manage a health profile, visualize weekly trends, and generate diet recommendations.

## Features

- Login-style landing page with Google sign-in placeholder for local use
- Symptom logging with weekly entries
- Exercise recommendations and curated workout links
- Data visualizations of symptom trends and flare risk
- Diet module using a meal plan prediction model
- Profile management for lab results and biometric inputs
- Local user data persistence under `user_data/{email}`

## Project Structure

- `h1.py` — Main Streamlit application entrypoint
- `utils/storage.py` — Profile and weekly log storage helpers
- `utils/model.py` — Model loading and feature building functions
- `mealplan/meals.py` — Meal plan recommendation data
- `mealplan/pcos_model.pkl` — Meal plan model binary
- `pcos_model.pkl` — PCOS flare risk prediction model
- `assets/` — Custom styles and images used in the app
- `user_data/` — Local saved profiles and weekly logs

## Requirements

- Python 3.10+ recommended
- Packages listed in `requirements.txt`

## Installation

1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

## Run the App

From the project root:

```powershell
streamlit run h1.py
```

Then open the URL shown in the terminal, usually `http://localhost:8501`.

## Local Usage Notes

- Local Google sign-in is disabled in the app; the login page shows a placeholder button.
- Data is stored locally under `user_data/<email>/`:
  - `profile.json`
  - `weekly_log.csv`
- Existing sample user folders are available for reference in `user_data/`.

## Troubleshooting

- If a model file is missing, ensure `pcos_model.pkl` and `mealplan/pcos_model.pkl` exist in the project root and `mealplan` directory, respectively.
- If visualization errors occur from missing data, add a profile and log at least one weekly symptom entry.

## Notes

This app is a prototype and not a medical diagnostic tool. Always consult a healthcare professional for medical advice.
