import pandas as pd
from dataclasses import dataclass
from typing import Any, Optional
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from numpy.typing import NDArray
import numpy as np


@dataclass
class ModelTrainer:
    x_data: pd.DataFrame
    y_data: pd.Series

    X_train: Optional[pd.DataFrame] = None
    X_val: Optional[pd.DataFrame] = None
    y_train: Optional[pd.DataFrame] = None
    y_val: Optional[pd.DataFrame] = None
    model: Optional[GradientBoostingClassifier] = None

    def split_data(self, test_size: float = 0.20, random_state: bool = True):
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            self.x_data, self.y_data, test_size=test_size, random_state=random_state
        )

    def train(
        self, random_state: int, params: dict[str, Any]
    ) -> GradientBoostingClassifier:
        if self.X_train is None or self.y_train is None:
            raise RuntimeError("Call split_data() before train()")

        self.model = GradientBoostingClassifier(random_state=random_state, **params)

        self.model.fit(self.X_train, self.y_train)

        return self.model

    def predict(self, X: pd.DataFrame | None = None) -> NDArray[np.float64]:
        if self.model is None:
            raise RuntimeError("Call train() before predict()")

        if X is None:
            if self.X_val is None:
                raise RuntimeError(
                    "No validation set. Call split_data() first or pass a dataframe in"
                )
            X = self.X_val

        return self.model.predict(X)
