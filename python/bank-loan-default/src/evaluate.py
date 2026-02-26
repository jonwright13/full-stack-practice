from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
from numpy.typing import NDArray
import numpy as np
from pathlib import Path
from typing import Any


def evaluate(
    y_val: pd.DataFrame,
    y_pred: NDArray[np.float64],
    X_val: pd.DataFrame,
    output_path: str | Path = "data/Predictions.csv",
    export: bool = False,
):
    # Calculate the accuracy of the prediction to the validation training set
    accuracy = accuracy_score(y_val, y_pred)

    # Calculate the F1-Score
    f1 = f1_score(y_val, y_pred, average="binary")

    # Combine prediction back into dataset
    predictions = pd.Series(y_pred, name="Prediction")
    merge1 = pd.concat([X_val.reset_index(drop=True), predictions], axis=1)
    merge2 = pd.concat([y_val.reset_index(drop=True), merge1], axis=1)

    # Export predictions to a csv
    if export:
        merge2.to_csv(output_path)
        print(f"Predictions saved to {output_path}")

    return {
        "accuracy": float(accuracy),
        "f1": float(f1),
        "results": merge2,
    }
