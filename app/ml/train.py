import joblib
import numpy as np 
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score
)

def train_model(model, X, y, version):
    model.fit(X, y)
    joblib.dump(model, f"models/gld_model_{version}.pkl")

    preds = model.predict(X)
    return {
        "rmse": np.sqrt(mean_squared_error(y, preds)),
        "mae": mean_absolute_error(y, preds),
        "mape": np.mean(np.abs((y - preds) / y)) * 100,
        "r2": r2_score(y, preds),
        "samples": len(y)
    }