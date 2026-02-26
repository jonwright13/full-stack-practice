import pandas as pd

from src.preprocess import preprocess_data
from src.train import ModelTrainer
from src.config import PARAMETERS


def test_split_data_creates_train_and_val(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    trainer = ModelTrainer(x_data=X, y_data=y)
    trainer.split_data(test_size=0.4, random_state=42)

    assert trainer.X_train is not None
    assert trainer.X_val is not None
    assert trainer.y_train is not None
    assert trainer.y_val is not None

    # sizes add up
    assert len(trainer.X_train) + len(trainer.X_val) == len(X)
    assert len(trainer.y_train) + len(trainer.y_val) == len(y)


def test_train_requires_split_first(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)
    trainer = ModelTrainer(x_data=X, y_data=y)

    try:
        trainer.train(random_state=42, params=PARAMETERS)
    except RuntimeError:
        assert True
    else:
        assert False, "Expected RuntimeError when calling train() before split_data()"


def test_train_and_predict_length_matches_val(raw_bank_df: pd.DataFrame):
    y, X = preprocess_data(raw_bank_df)

    trainer = ModelTrainer(x_data=X, y_data=y)
    trainer.split_data(test_size=0.4, random_state=42)
    trainer.train(random_state=42, params=PARAMETERS)

    y_pred = trainer.predict()  # default should predict on X_val
    assert len(y_pred) == len(trainer.X_val)
