from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import joblib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path("model.joblib")
pipeline = None
LABEL_DISPLAY_MAP = {
    "action_request": "Action Request",
    "information": "Information",
    "complaint": "Complaint",
    "urgent": "Urgent",
    "spam": "Spam",
}
CLASS_NAMES = None

def load_model():
    global pipeline
    global CLASS_NAMES
    if MODEL_PATH.exists():
        try:
            pipeline = joblib.load(MODEL_PATH)
            try:
                CLASS_NAMES = list(getattr(pipeline[-1], "classes_"))
            except Exception:
                CLASS_NAMES = None
        except Exception:
            pipeline = None

load_model()

class EmailInput(BaseModel):
    email: str

@app.post("/classify")
def classify_email(data: EmailInput):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Train the model and ensure model.joblib exists.")

    text = data.email or ""
    if not isinstance(text, str) or not text.strip():
        raise HTTPException(status_code=400, detail="Invalid email text.")
    try:
        proba = pipeline.predict_proba([text])[0]
        classes = CLASS_NAMES or list(getattr(pipeline[-1], "classes_", []))
        pred_idx = int(proba.argmax())
    except AttributeError:
        pred_label = pipeline.predict([text])[0]
        proba = None
        classes = CLASS_NAMES or []

    if proba is not None and classes and len(classes) == len(proba):
        probabilities = {}
        for i, cls in enumerate(classes):
            display = LABEL_DISPLAY_MAP.get(cls, str(cls))
            probabilities[display] = float(round(proba[i], 4))
        predicted_label = classes[pred_idx]
    else:
        probabilities = None
        predicted_label = pred_label if 'pred_label' in locals() else None

    predicted_class = LABEL_DISPLAY_MAP.get(predicted_label, str(predicted_label))

    return {
        "message": "Classification successful",
        "probabilities": probabilities,
        "predicted_class": predicted_class,
        "model_status": "loaded" if pipeline is not None else "unavailable",
    }

@app.get("/")
def read_root():
    return {
        "message": "Email Classifier API is running",
        "model_status": "loaded" if pipeline is not None else "unavailable",
    }
