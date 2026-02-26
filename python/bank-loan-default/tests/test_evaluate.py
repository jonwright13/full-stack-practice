import pandas as pd

from src.evaluate import evaluate


def test_evaluate_writes_csv_and_returns_metrics(tmp_path):
    # minimal example inputs
    X_val = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    y_val = pd.Series([0, 1], name="Default_On_Payment")
    y_pred = [0, 1]

    out_file = tmp_path / "preds.csv"
    out = evaluate(
        y_val=y_val, y_pred=y_pred, X_val=X_val, output_path=out_file, export=True
    )

    # metrics returned and sane
    assert 0.0 <= out["accuracy"] <= 1.0
    assert 0.0 <= out["f1"] <= 1.0

    # file written
    assert out_file.exists()

    # CSV contains expected columns
    df = pd.read_csv(out_file)
    assert "Prediction" in df.columns
    assert "Default_On_Payment" in df.columns  # y_val merged back in
    assert len(df) == len(X_val)
