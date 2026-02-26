# Preprocessing config
EXCLUDE_FEATURES = [
    "Customer_ID",
    "Default_On_Payment",
    "Count",
    "Credit_Amount",
    "Foreign_Worker",
]
TARGET_COL = "Default_On_Payment"

EXPLOYMENT_BINS = [0, 11, 24, 48, float("inf")]
EMPLOYMENT_LABELS = ["<1 Year", "1-2 Years", "2-4 Years", "4-6 Years"]
EMPLOYMENT_COL = "Duration_in_Months"

AGE_BINS = [19, 25, 35, 45, 55, 65, float("inf")]
AGE_LABELS = [
    "19-25 Years",
    "26-35 Years",
    "36-45 Years",
    "46-55 Years",
    "56-65 Years",
    "66+ Years",
]
AGE_COL = "Age"

# Training config
PARAMETERS = {"learning_rate": 0.15, "max_depth": 5, "n_estimators": 500}
