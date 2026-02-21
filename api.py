from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

# Load model
ml_model = joblib.load("heart_disease_model.pkl")

app = FastAPI(
    title="AI Cardiovascular Risk API",
    description="Production-ready ML API for Heart Disease Risk Prediction",
    version="1.0"
)

# Request Schemafrom fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib

# ================= LOAD MODEL =================
ml_model = joblib.load("heart_disease_model.pkl")

app = FastAPI(
    title="AI Cardiovascular Risk API",
    description="Production-ready ML API for Heart Disease Risk Prediction",
    version="1.0"
)

# ================= REQUEST SCHEMA =================
class PatientData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

# ================= HEALTH CHECK =================
@app.get("/")
def home():
    return {"message": "AI Cardiovascular Risk Prediction API Running"}

# ================= PREDICTION ENDPOINT =================
@app.post("/predict")
def predict(data: PatientData):

    input_data = np.array([[
        data.age,
        data.sex,
        data.cp,
        data.trestbps,
        data.chol,
        data.fbs,
        data.restecg,
        data.thalach,
        data.exang,
        data.oldpeak,
        data.slope,
        data.ca,
        data.thal
    ]])

    prediction = ml_model.predict(input_data)
    probability = ml_model.predict_proba(input_data)

    risk_score = float(probability[0][1] * 100)
    confidence = float(np.max(probability) * 100)

    return {
        "prediction": int(prediction[0]),
        "risk_score_percent": round(risk_score, 2),
        "confidence_percent": round(confidence, 2)
    }

class PatientData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@app.get("/")
def home():
    return {"message": "AI Cardiovascular Risk Prediction API Running"}

@app.post("/predict")
def predict(data: PatientData):

    input_data = np.array([[
        data.age,
        data.sex,
        data.cp,
        data.trestbps,
        data.chol,
        data.fbs,
        data.restecg,
        data.thalach,
        data.exang,
        data.oldpeak,
        data.slope,
        data.ca,
        data.thal
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    risk_score = float(probability[0][1] * 100)
    confidence = float(np.max(probability) * 100)

    return {
        "prediction": int(prediction[0]),
        "risk_score_percent": round(risk_score, 2),
        "confidence_percent": round(confidence, 2)
    }
