import pandas as pd

from src.preprocess import preprocess_data


def test_preprocess_splits_target_and_features(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    assert len(y) == len(raw_bank_df)
    assert len(X) == len(raw_bank_df)

    # target removed from features
    assert "Default_On_Payment" not in X.columns


def test_preprocess_excludes_specified_columns(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    # explicitly excluded columns should not be in X
    for col in ["Customer_ID", "Count", "Credit_Amount"]:
        assert col not in X.columns


def test_preprocess_creates_binned_features(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    assert "Years_in_Employment" in X.columns
    assert "Age_Range" in X.columns


def test_preprocess_drops_redundant_columns(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    # you drop these after binning
    assert "Age" not in X.columns
    assert "Duration_in_Months" not in X.columns
    assert "Foreign_Worker" not in X.columns


def test_preprocess_returns_copy_not_view(raw_bank_df: pd.DataFrame):
    # Ensure preprocess doesn't mutate input df
    df = raw_bank_df.copy()
    _y, _X = preprocess_data(df)

    # Original df should still have original columns
    assert "Age" in df.columns
    assert "Duration_in_Months" in df.columns
