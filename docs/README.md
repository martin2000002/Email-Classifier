# Project Docs

## Overview
- Email classification API using TF-IDF + Logistic Regression.
- Classes: Action Request, Information, Complaint, Urgent, Spam.
- Language: English-only dataset.

## Setup
1. Create venv: `./setup.ps1` (Windows) or `./setup.sh` (Linux/Mac)
2. Activate venv: `./venv/Scripts/Activate.ps1` or `source venv/bin/activate`

## Workflow
- Generate data: `python data/generate_dataset.py`
- Train model: `python code/backend/train.py`
- Run API: `cd code/backend && python -m uvicorn main:app --reload`
- Frontend: open `code/frontend/index.html`

## API Contract
POST `/classify`
Request:
```json
{ "email": "Email text with \n line breaks" }
```
Response:
```json
{
  "message": "Classification successful",
  "predicted_class": "Urgent",
  "probabilities": {
    "Action Request": 0.0312,
    "Information": 0.0123,
    "Complaint": 0.0401,
    "Urgent": 0.9015,
    "Spam": 0.0149
  },
  "model_status": "loaded"
}
```

## Validation Summary
- Best CV mean ~0.934 with `ngram=(1,2)`, `max_features=20000`, `C=50`.
- Test accuracy ~0.96 (held-out split).
