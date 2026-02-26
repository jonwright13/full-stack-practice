import pandas as pd
from typing import Any, Tuple
from sklearn.preprocessing import LabelEncoder

from src.config import (
    EXCLUDE_FEATURES,
    TARGET_COL,
    EXPLOYMENT_BINS,
    EMPLOYMENT_LABELS,
    EMPLOYMENT_COL,
    AGE_BINS,
    AGE_LABELS,
    AGE_COL,
)


def preprocess_data(data: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    # Split data into features and target and drop specific columns for customer ID, target, and count
    x_target_columns = [col for col in data.columns if col not in EXCLUDE_FEATURES]
    Y_data, X_data = split_data(data, TARGET_COL, x_target_columns)

    # Categorise employment duration into years
    X_data["Years_in_Employment"] = categorise(
        X_data[EMPLOYMENT_COL], EXPLOYMENT_BINS, EMPLOYMENT_LABELS
    )

    # Categorise ages into age_range
    X_data["Age_Range"] = categorise(X_data[AGE_COL], AGE_BINS, AGE_LABELS)

    # Drop redundant columns after binning
    cols_to_drop = [AGE_COL, EMPLOYMENT_COL]
    X_data = drop_columns(X_data, cols_to_drop)

    encoded_x_data = encoding(X_data)

    return Y_data, encoded_x_data


def split_data(
    data: pd.DataFrame, y_header: str, x_headers: list[str]
) -> Tuple[pd.Series, pd.DataFrame]:
    # Split data into features and target and drop specific columns for customer ID, target, and count
    X_data = data.loc[:, x_headers].copy()
    Y_data = data.loc[:, y_header].copy()

    return Y_data, X_data


def categorise(
    series: pd.Series,
    bins: list[int],
    labels: list[str],
) -> pd.Series:

    return pd.cut(series, bins=bins, labels=labels, include_lowest=True)


def drop_columns(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return data.drop(columns, axis="columns", errors="ignore")


def encoding(X_data: pd.DataFrame):
    """
    Encode categorical labels with numerical ones using LabelEncoder
    """

    # Create a blank dataframe for the encoded categorical data
    cat_data_encoded = pd.DataFrame()

    for col in X_data.columns:
        if X_data[col].dtype in ["object", "category"]:

            # Initialize the LabelEncoder
            label_encoder = LabelEncoder()

            # Fit and transform the categorical data
            cat_data_encoded[col] = label_encoder.fit_transform(X_data[col])

    # combine with numerical data
    return pd.concat(
        [
            cat_data_encoded,
            X_data[
                [
                    col
                    for col in X_data.columns
                    if X_data[col].dtype in ["int64", "float64"]
                ]
            ],
        ],
        axis=1,
    )
