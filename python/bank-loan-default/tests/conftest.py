import pandas as pd
import pytest


@pytest.fixture
def raw_bank_df() -> pd.DataFrame:
    # Minimal sytnthetic dataset
    return pd.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4, 5],
            "Count": [1, 1, 1, 1, 1],
            "Default_On_Payment": [0, 1, 0, 1, 0],
            "Credit_Amount": [1000, 2000, 1500, 3000, 1200],
            "Duration_in_Months": [6, 18, 36, 60, 80],  # includes >72 edge
            "Age": [22, 30, 40, 55, 76],  # includes >75 edge
            "Foreign_Worker": ["Yes", "Yes", "No", "Yes", "Yes"],
            "Job_Type": ["A", "B", "A", "C", "B"],  # categorical
            "Housing": ["rent", "own", "own", "rent", "free"],  # categorical
        }
    )
