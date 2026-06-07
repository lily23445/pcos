# 1. Imports
import streamlit as st
import pandas as pd
import joblib
from meals import meal_plans  # your meal plan dictionary

# 2. Load model
model = joblib.load("pcos_.pkl")

# 3. Streamlit UI
st.title("🩺 Health Category & Diet Recommendation")

# Collect user inputs
age = st.number_input("Age", min_value=10, max_value=100)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=150.0)
height = st.number_input("Height (cm)", min_value=100.0, max_value=220.0)
preference = st.selectbox("Diet Preference", ["vegetarian", "non-vegetarian", "vegan"])
tsh = st.number_input("TSH (miu/L)")
fsh_lh = st.number_input("FSH/LH ratio")
amh = st.number_input("AMH (ng/ml)")
prl = st.number_input("Prolactin (ng/ml)")
waist = st.number_input("Waist (inches)")
cycle_length = st.number_input("Cycle Length (days)")
hair_loss = st.selectbox("Hair Loss", [0, 1])
skin_darkening = st.selectbox("Skin Darkening", [0, 1])

# 4. Predict and Recommend
if st.button("Get My Meal Plan"):
    user_input = {
        "age_yrs": age,
        "weight_kg": weight,
        "heightcm": height,
        "bmi": weight / ((height / 100) ** 2),
        "tsh_miu/l": tsh,
        "fsh/lh": fsh_lh,
        "amhng/ml": amh,
        "prlng/ml": prl,
        "waistinch": waist,
        "cycle_lengthdays": cycle_length,
        "hair_lossy/n": hair_loss,
        "skin_darkening_y/n": skin_darkening
    }

    user_df = pd.DataFrame([user_input])
    predicted_category = model.predict(user_df)[0]
    meals = meal_plans.get(predicted_category, {}).get(preference.lower(), [])

    st.write(f"Health Category: **{predicted_category}**")
    st.success("Recommended Meal Plan:")
    for meal in meals:
        st.markdown(f"- {meal}")