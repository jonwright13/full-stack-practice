from src.io import import_data
from src.preprocess import preprocess_data
from src.train import ModelTrainer
from src.evaluate import evaluate

from src.config import PARAMETERS


def run() -> None:
    fpath = "data/bank_loan_dataset.xlsx"
    sname = "Data"

    data = import_data(
        fpath=fpath, sheet_name=sname, header=2, exclude_columns=["Unnamed"]
    )

    Y_data, X_data = preprocess_data(data)

    # Initialise model trainer
    model = ModelTrainer(x_data=X_data, y_data=Y_data)

    # Split data
    model.split_data(test_size=0.20, random_state=True)

    # Train data
    model.train(random_state=42, params=PARAMETERS)

    # Make prediction
    y_pred = model.predict()

    evaluate(Y_val=model.y_val, Y_pred=y_pred, X_val=model.X_val)


if __name__ == "__main__":
    run()
