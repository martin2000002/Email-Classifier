# Email Classifier (Group 10)

## Project Overview and Purpose
This project is an **Email Intent Classifier** designed to help users organize their inbox by automatically categorizing emails into five distinct intents: **Action Request, Information, Complaint, Urgent, and Spam**.

The goal is to streamline email management for employees, customer service representatives, and students, allowing them to prioritize urgent tasks and filter out noise. The system uses a **Machine Learning pipeline (TF-IDF + Logistic Regression)** trained on a synthetic dataset generated via LLMs to ensure privacy and control over data distribution.
---

## Video Link


---

## Installation and Setup Instructions

### Prerequisites
- **Python 3.9+**
- **Git** (optional, for cloning)

### 1. Clone or Download the Repository
```powershell
git clone <repository-url>
cd group10_project
```

### 2. Set Up the Environment
We provide a setup script to create a virtual environment and install dependencies.

**Windows (PowerShell):**
```powershell
./setup.ps1
./venv/Scripts/activate
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

## How to Run the Program and Reproduce Results

### 1. Generate the Dataset (Optional)
If you want to regenerate the training data (requires an OpenAI API Key in `data/.env`):
```powershell
# Create .env file with OPENAI_API_KEY=sk-...
cd data
python generate_dataset.py
cd ..
```
*Note: The dataset is already included.*

### 2. Train the Model
Train the Logistic Regression model using the dataset. This script performs cross-validation and saves the best model to `code/backend/model.joblib`.
```powershell
python "code/backend/train.py" --no-plot
```
*Remove `--no-plot` to see the interactive performance heatmaps.*

### 3. Start the Backend API
Launch the FastAPI server to serve predictions.
```powershell
python "code/backend/main.py"
```
The API will run at `http://127.0.0.1:8000`.

### 4. Run Tests
Verify that everything is working correctly by running the test suite:
```powershell
pytest -q
```

### 5. Launch the Frontend
Simply open the `code/frontend/index.html` file in your web browser.
- Enter an email text.
- Click **Classify**.
- View the predicted category and confidence scores.

---

## Technologies and Libraries Used

- **Language:** Python 3.9+
- **Machine Learning:**
  - `scikit-learn`: TF-IDF Vectorizer, Logistic Regression, Stratified K-Fold CV.
  - `joblib`: Model persistence.
  - `numpy` & `matplotlib`: Data manipulation and visualization.
- **Backend:**
  - `FastAPI`: High-performance web framework.
  - `Uvicorn`: ASGI server.
  - `Pydantic`: Data validation.
- **Frontend:** HTML5, CSS3 (Modern Dark Theme), JavaScript (Fetch API).
- **Data Generation:** OpenAI API (Agents SDK), `python-dotenv`.

---

## Author(s) and Contribution Summary

**Group 10**
- **Sakash Khanna**
- **Martín Montero**

### Contribution Summary
- **Research & Planning:** Joint effort in defining the 5 categories and selecting the ML approach (TF-IDF + LR).
- **Dataset Generation:** Martín: Implemented the LLM-based generator to create diverse, labeled email examples.
- **Backend Development:** Martín: Built the FastAPI service, training pipeline, and integration logic.
- **Frontend Development:** Sakash: Designed the web interface and connected it to the classification API.
- **Testing & Documentation:** Sakash: Created the test suite and wrote the project documentation.

---

### Honor Code Statement
*We affirm our adherence to the honor code and ethical use of Large Language Models (LLMs) for this project. We used LLMs primarily to generate the synthetic labeled dataset for training our model, ensuring no private data was compromised.*
