# Bank Loan Default Prediction

A structured machine learning pipeline that predicts loan default using a Gradient Boosting Classifier.

This project refactors an interview-style data science task into a clean, modular, testable Python package using a `src/` layout and pytest.

---

## 🎯 Objective

Given a bank loan dataset, predict whether a customer will default on payment.

The project demonstrates:

- Structured preprocessing pipeline
- Feature engineering (binning + categorical handling)
- Train/validation splitting
- Gradient Boosting model training
- Evaluation (Accuracy + F1)
- Reproducible training via fixed random states
- Test coverage for preprocessing and training logic
- Modular architecture suitable for production extension

---

## 🏗 Project Structure

```Code
bank-loan-default/
│
├── src/
│   ├── __init__.py
│   ├── io.py
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
│   └── config.py
│
├── scripts/
│   └── run_training.py
│
├── tests/
│   ├── test_preprocess.py
│   ├── test_train.py
│   └── test_evaluate.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🔄 Pipeline Overview

### 1. Data Loading

- Excel dataset loaded into a Pandas DataFrame
- Unnamed columns removed

### 2. Preprocessing

- Target (`Default_On_Payment`) separated
- Irrelevant features removed:
  - `Customer_ID`
  - `Count`
  - `Credit_Amount`

- Feature engineering:
  - `Duration_in_Months` → `Years_in_Employment` (binned)
  - `Age` → `Age_Range` (binned)

- Redundant columns dropped
- Clean DataFrame returned

### 3. Train/Validation Split

- `train_test_split`
- Configurable `test_size`
- Deterministic via `random_state`

### 4. Model Training

- `GradientBoostingClassifier`
- Parameters loaded from `config.py`

### 5. Evaluation

- Accuracy Score
- F1 Score
- Validation predictions exported to `Predictions.csv`

---

## 🚀 Running the Project

From project root:

```bash
python -m scripts.run_training
```

This will:

- Train the model
- Print evaluation metrics
- Generate `Predictions.csv`

---

## 🧪 Running Tests

```bash
pytest
```

Test coverage includes:

- Preprocessing correctness
- Column exclusion logic
- Binning behaviour
- Train/validation split integrity
- Model training guard conditions
- Evaluation output & CSV generation

---

## 🐳 Docker (Optional)

Build and run:

```bash
docker build -t bank-loan-default .
docker run --rm bank-loan-default
```

---

## 🧠 Engineering Notes

This project intentionally:

- Avoids `inplace=True`
- Uses explicit feature selection
- Avoids silent pandas mutation
- Separates preprocessing, training, and evaluation concerns
- Supports modular extension (e.g. API serving, model serialization)

---

## 📌 Future Improvements

- Add fit/transform Preprocessor class to avoid leakage
- Add OneHotEncoder or Pipeline integration
- Add model serialization (joblib)
- Expose FastAPI endpoint for predictions
- Add CI pipeline
