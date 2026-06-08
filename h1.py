import streamlit as st
from pathlib import Path
import os
from datetime import date
import utils.storage as store
from utils.model import get_mealplan_model, build_mealplan_features, get_model, build_features
from mealplan.meals import meal_plans
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ---------- Helpers ----------
def safe_image(path, **kwargs):
    if os.path.exists(path):
        st.image(path, **kwargs)
    else:
        st.error(f"Image not found: {path}")


def inject_local_css(path: str):
    if os.path.exists(path):
        css = Path(path).read_text("utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Only inject CSS if file exists
if os.path.exists("assets/theme.css"):
    inject_local_css("assets/theme.css")


# ---------- LOGIN PAGE ----------
def login_page():
    st.title("Login Page")

    col1, _, col2 = st.columns([4, 0.5, 2])

    with col1:
        safe_image("assets/login.png", width=600)

    with col2:
        st.markdown(
            """
            <div style="
                 background: var(--secondary-background-color);
                 padding: 2rem 1.5rem;
                 border-radius: 0.75rem;
                 box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                 text-align:center;">
                 <div style="font-size:3rem;margin-bottom:.4rem;">🩺</div>
                 <h2 style="margin:0 0 .4rem;">PCOS Tracker</h2>
                 <p style="margin:0 0 1rem;">Continue with your Google account</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Streamlit Cloud (real Google OAuth) ---
        # --- Streamlit Cloud (real Google OAuth) ---
        if hasattr(st, "login"):
            if st.button("Sign in with Google", type="primary"):
                st.login("google")  # ✅ Remove st.stop() — let it redirect naturally
        else:
            st.button("Sign in with Google", disabled=True)
            st.info("Google login works once you deploy to Streamlit Cloud.")


# ---------- DASHBOARD PAGE ----------
def dashboard_page():
    st.title("Health Dashboard")
    st.success(f"Welcome, {st.session_state.email}!")

    if st.button("Log Out"):
        if hasattr(st, "logout"):
            st.logout()  # Cloud logout
        st.session_state.logged_in = False
        st.session_state.email = None
        st.rerun()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Symptoms Log", "Exercise Recommendation", "Data Visuals", "Diet Module", "Profile/Settings"]
    )

    # ---- Symptoms Log ----
    with tab1:
        st.header("Log Symptoms")
        col1, col2 = st.columns([3, 5])

        with col1:
            safe_image("assets/symptomlog.png", use_container_width=True)

        with col2:
            with st.form("symptom_form"):
                st.subheader("Symptoms Log")
                week_start = st.date_input("Week starting from", date.today())
                weight_gain = st.radio("Weight gain", ["Yes", "No"], horizontal=True)
                hair_growth = st.radio("Hair growth", ["Yes", "No"], horizontal=True)
                skin_darkening = st.radio("Skin darkening", ["Yes", "No"], horizontal=True)
                pimples = st.radio("Pimples", ["Yes", "No"], horizontal=True)
                hair_loss = st.radio("Hair loss", ["Yes", "No"], horizontal=True)
                other_symptoms = st.text_area("Other symptoms / notes", height=100)

                if st.form_submit_button("Save Symptoms"):
                    entry = {
                        "WeekOf": week_start.isoformat(),
                        "Weight gain(Y/N)": 1 if weight_gain == "Yes" else 0,
                        "Hair growth(Y/N)": 1 if hair_growth == "Yes" else 0,
                        "Skin darkening(Y/N)": 1 if skin_darkening == "Yes" else 0,
                        "Pimples(Y/N)": 1 if pimples == "Yes" else 0,
                        "Hair loss(Y/N)": 1 if hair_loss == "Yes" else 0,
                        "Notes": other_symptoms,
                    }
                    store.append_weekly(entry, st.session_state.email)
                    st.success("Symptoms logged successfully!")

    # ---- Exercise Recommendation ----
    with tab2:
        st.header("Exercise Recommendation Module")
        col1, col2, col3 = st.columns([90, 120, 110])

        with col1:
            safe_image("assets/excercise.png", use_container_width=True)

        with col2:
            st.info("""
            Regular exercise can help manage PCOS symptoms by improving insulin sensitivity,
            balancing hormones, supporting weight management,
            and reducing stress. A balanced mix of cardio, strength training, and relaxation exercises works best.
            """)
            with st.expander("1️. Cardio / Aerobic Exercises"):
                st.write(
                    "• Do 3–5 times per week (30–45 minutes)\n• Brisk walking, jogging, cycling, swimming, or dancing")

            with st.expander("2️. Strength Training"):
                st.write("• Do 2–3 times per week\n• Bodyweight exercises, resistance bands, or weights")

            with st.expander("3️. HIIT"):
                st.write("• Do 1–2 times per week\n• Short bursts of high effort followed by rest")

            with st.expander("4️. Yoga & Stress Relief"):
                st.write("• Yoga, Pilates, stretching routines to reduce cortisol and balance hormones")

        with col3:
            st.subheader("YouTube Exercise Recommendations")
            st.markdown("**[Chloe Ting](https://www.youtube.com/watch?v=2pLT-olgUJs)** – HIIT & strength workouts")
            st.markdown("**[MadFit](https://youtu.be/eQdX2_k8FIM)** – Dance cardio & yoga")
            st.markdown("**[Yoga With Adriene](https://www.youtube.com/watch?v=v7AYKMP6rOE)** – Gentle yoga flows")

    # ---- Data Visuals ----
    with tab3:
        st.header("View Your Cycle (Data Visuals)")
        email = st.session_state.get("email", None)

        try:
            profile = store.load_profile(email)
            weekly = store.read_weekly(email)

            if not profile or weekly.empty:
                st.warning("Please complete your profile and log at least one symptom entry.")
            else:
                st.write("✅ Weekly Data Snapshot:", weekly.head())
                st.progress(min(len(weekly) / 4.0, 1.0), text=f"{len(weekly)}/4 weeks logged")

                X = build_features(profile, weekly)
                prob = get_model().predict_proba(X)[0, 1] * 100
                st.metric("PCOS-flare risk", f"{prob:.1f}%")

                df = weekly.copy()
                df.columns = df.columns.str.strip()
                df["WeekOf"] = pd.to_datetime(df["WeekOf"], errors="coerce")
                df.set_index("WeekOf", inplace=True)
                symptom_cols = [c for c in df.columns if c not in ["total_symptoms", "Notes"]]
                df[symptom_cols] = df[symptom_cols].fillna(0)

                fig, ax = plt.subplots(figsize=(18, 9))
                sns.heatmap(df[symptom_cols].T, cmap="YlGnBu", cbar=True, linewidths=0.5, linecolor='gray', ax=ax)
                ax.set_title("Symptom Presence Heatmap")
                st.pyplot(fig)

                df["total_symptoms"] = df[symptom_cols].sum(axis=1)
                fig2, ax2 = plt.subplots(figsize=(18, 9))
                ax2.bar(df.index, df["total_symptoms"], color="skyblue")
                ax2.set_title("Total Symptoms per Week")
                st.pyplot(fig2)
        except Exception as e:
            st.error(f"Error loading data visuals: {str(e)}")

    # ---- Diet Module ----
    with tab4:
        st.header("Diet Module")

        try:
            col1, col2 = st.columns([5, 3])
            with col1:
                safe_image("assets/dietmodule.png", use_container_width=True)

            with col2:
                email = st.session_state.get("email")  # FIX: Define email here!
                profile = store.load_profile(email)

                if not profile:
                    st.warning("Please complete your profile first in the Profile/Settings tab.")
                else:
                    food_pref = st.selectbox("Choose your diet preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])

                    if st.button("Generate Meal Plan"):
                        try:
                            model = get_mealplan_model()
                            X = build_mealplan_features(profile)
                            category = model.predict(X)[0]
                            st.success(f"Predicted Health Category: **{category}**")

                            plan = meal_plans.get(category.lower(), {}).get(food_pref.lower(), [])
                            if plan:
                                st.subheader(f"Recommended {food_pref} Meal Plan:")
                                for idx, meal in enumerate(plan, 1):
                                    st.write(f"{idx}. {meal}")
                            else:
                                st.warning("No meal plan found for this selection.")
                        except FileNotFoundError:
                            st.error("Meal plan model file not found. Please ensure 'mealplan/pcos_model.pkl' exists.")
                        except Exception as e:
                            st.error(f"Error generating meal plan: {str(e)}")
        except Exception as e:
            st.error(f"Error in Diet Module: {str(e)}")

    # ---- Profile / Settings ----
    with tab5:
        st.header("Manage Profile / Settings")

        try:
            col1, col2 = st.columns([10, 8])
            with col1:
                safe_image("assets/profile.png", use_container_width=True)

            with col2:
                email = st.session_state.get("email")
                profile = store.load_profile(email)

                if not isinstance(profile, dict):
                    profile = {}

                with st.form("profile_form"):
                    name = st.text_input("Name", value=profile.get("name", ""))
                    age = st.number_input("Age (years)", 1, 100, int(profile.get("Age", 25)))
                    bmi = st.number_input("BMI", 0.0, format="%.2f", value=float(profile.get("BMI", 0.0)))
                    waist = st.number_input("Waist (cm)", 0.0, format="%.1f", value=float(profile.get("Waist", 0.0)))
                    tsh = st.number_input("TSH (mIU/L)", 0.0, format="%.2f", value=float(profile.get("TSH", 0.0)))
                    lh = st.number_input("LH (mIU/mL)", 0.0, format="%.2f", value=float(profile.get("LH", 0.0)))
                    fsh = st.number_input("FSH (mIU/mL)", 0.0, format="%.2f", value=float(profile.get("FSH", 0.0)))
                    amh = st.number_input("AMH (ng/mL)", 0.0, format="%.2f", value=float(profile.get("AMH", 0.0)))
                    prl = st.number_input("PRL (ng/mL)", 0.0, format="%.2f", value=float(profile.get("PRL", 0.0)))

                    if st.form_submit_button("Update Profile"):
                        store.save_profile(
                            st.session_state.email,
                            {
                                "name": name, "Age": age, "BMI": bmi, "Waist": waist,
                                "AMH": amh, "TSH": tsh, "LH": lh, "FSH": fsh, "PRL": prl,
                                "LastUpdated": date.today().isoformat(),
                            }
                        )
                        st.success("Profile saved ✔️")
                        st.rerun()
        except Exception as e:
            st.error(f"Error in Profile/Settings: {str(e)}")


# ---------- AUTH CHECK ----------
# ---------- AUTH CHECK ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🐛 TEMP DEBUG — remove after fixing
st.write("is_logged_in:", st.user.is_logged_in if hasattr(st, "user") else "no st.user")
st.write("session logged_in:", st.session_state.logged_in)

if hasattr(st, "user") and st.user and st.user.is_logged_in:
    st.session_state.logged_in = True
    st.session_state.email = st.user.email

if not st.session_state.logged_in:
    login_page()
    st.stop()
else:
    dashboard_page()