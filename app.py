import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Cardiovascular Risk System",
    page_icon="❤️",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🫀 Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["❤️ Risk Prediction", "📘 About"]
)

# =====================================================
# RISK PREDICTION PAGE
# =====================================================

if page == "❤️ Risk Prediction":

    st.title("AI-Based Cardiovascular Risk Assessment System")
    st.markdown("Clinical Decision Support Dashboard")

    # ================= INPUT MODE =================
    input_mode = st.radio(
        "Select Input Mode",
        ["📝 Manual Entry", "🎲 Random Sample Patient"]
    )

    # ================= RANDOM MODE =================
    if input_mode == "🎲 Random Sample Patient":

        age = np.random.randint(30, 75)
        sex_val = np.random.randint(0, 2)
        cp = np.random.randint(0, 4)
        trestbps = np.random.randint(100, 170)
        chol = np.random.randint(150, 300)
        fbs = np.random.randint(0, 2)
        restecg = np.random.randint(0, 3)
        thalach = np.random.randint(90, 190)
        exang = np.random.randint(0, 2)
        oldpeak = round(np.random.uniform(0, 4), 1)
        slope = np.random.randint(0, 3)
        ca = np.random.randint(0, 4)
        thal = np.random.randint(0, 3)

        sex_display = "Male" if sex_val == 1 else "Female"
    
        st.info("Random patient generated for demonstration.")
    
        st.subheader("🧑 Generated Patient Details")
    
        random_data = {
            "Age": age,
            "Sex": sex_display,
            "Chest Pain Type": cp,
            "Resting Blood Pressure": trestbps,
            "Cholesterol": chol,
            "Fasting Blood Sugar >120": fbs,
            "Rest ECG": restecg,
            "Max Heart Rate": thalach,
            "Exercise Induced Angina": exang,
            "ST Depression": oldpeak,
            "Slope": slope,
            "Major Vessels": ca,
            "Thal": thal
        }
    
        st.table(random_data)


    else:
        # ================= MANUAL ENTRY =================
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 1, 120, 45)
            sex = st.selectbox("Sex", ["Male", "Female"])
            cp = st.selectbox("Chest Pain Type (0-3)", [0,1,2,3])
            trestbps = st.number_input("Resting Blood Pressure", 80, 200, 120)
            chol = st.number_input("Cholesterol Level", 100, 600, 220)
            fbs = st.selectbox("Fasting Blood Sugar >120", [0,1])

        with col2:
            restecg = st.selectbox("Rest ECG (0-2)", [0,1,2])
            thalach = st.number_input("Max Heart Rate", 60, 220, 150)
            exang = st.selectbox("Exercise Induced Angina", [0,1])
            oldpeak = st.number_input("ST Depression", 0.0, 10.0, 1.0)
            slope = st.selectbox("Slope (0-2)", [0,1,2])
            ca = st.selectbox("Major Vessels (0-4)", [0,1,2,3,4])
            thal = st.selectbox("Thal (0-2)", [0,1,2])

        sex_val = 1 if sex == "Male" else 0

    # ================= PREDICTION BUTTON =================
    if st.button("🔍 Predict Risk"):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "age": age,
                    "sex": sex_val,
                    "cp": cp,
                    "trestbps": trestbps,
                    "chol": chol,
                    "fbs": fbs,
                    "restecg": restecg,
                    "thalach": thalach,
                    "exang": exang,
                    "oldpeak": oldpeak,
                    "slope": slope,
                    "ca": ca,
                    "thal": thal
                }
            )

            if response.status_code == 200:

                result = response.json()
                risk_score = result["risk_score_percent"]
                confidence = result["confidence_percent"]

                # ================= RISK GAUGE =================
                st.subheader("📊 Risk Assessment")

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_score,
                    number={'suffix': "%"},
                    title={'text': "Heart Disease Risk"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "red"}
                    }
                ))

                st.plotly_chart(fig, use_container_width=True)

                st.metric("Prediction Confidence", f"{confidence:.2f}%")

                # ================= SEVERITY LEVEL =================
                if risk_score > 75:
                    severity = "Stage 3 – Severe Cardiac Risk"
                    st.error(severity)
                elif risk_score > 50:
                    severity = "Stage 2 – High Risk"
                    st.warning(severity)
                elif risk_score > 30:
                    severity = "Stage 1 – Moderate Risk"
                    st.info(severity)
                else:
                    severity = "Low Cardiovascular Risk"
                    st.success(severity)

                st.progress(int(risk_score))

                # ================= CLINICAL ANALYSIS =================
                st.subheader("🩺 Clinical Evaluation")

                if trestbps > 130:
                    st.error("Elevated Blood Pressure")
                if chol > 200:
                    st.error("High Cholesterol Level")
                if thalach < 100:
                    st.warning("Low Heart Rate Capacity")

                # ================= AI EXPLANATION =================
                st.subheader("🧠 AI Insight")

                factors = []
                if chol > 200:
                    factors.append("High Cholesterol")
                if trestbps > 130:
                    factors.append("Elevated Blood Pressure")
                if exang == 1:
                    factors.append("Exercise-Induced Angina")

                if factors:
                    st.info("Primary influencing factors: " + ", ".join(factors))
                else:
                    st.info("No major abnormal indicators detected.")

                # ================= RECOMMENDATIONS =================
                st.subheader("🤖 Clinical Recommendations")

                if risk_score > 60:
                    st.error("Immediate cardiology consultation advised.")
                elif risk_score > 35:
                    st.warning("Adopt heart-healthy lifestyle and monitor regularly.")
                else:
                    st.success("Maintain healthy lifestyle and preventive checkups.")

                # ================= SUMMARY =================
                st.subheader("📋 Clinical Summary")

                st.write(f"""
                Risk Score: {risk_score:.2f}%  
                Severity Level: {severity}  
                Confidence: {confidence:.2f}%  
                Recommended Action: {"Consult Cardiologist" if risk_score > 60 else "Lifestyle Monitoring"}
                """)

            else:
                st.error("API Error. Ensure FastAPI server is running.")

        except:
            st.error("Unable to connect to API. Start FastAPI first.")

# =====================================================
# ABOUT PAGE
# =====================================================

else:
    st.title("📘 About This System")

    st.write("""
    AI-Based Cardiovascular Risk Assessment System

    Architecture:
    - Streamlit Frontend
    - FastAPI Backend
    - Random Forest Model
    - REST API Integration

    This system is designed as a Clinical Decision Support Tool.
    It is not a substitute for professional medical advice.
    """)
