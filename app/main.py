import os
import joblib
# import pandas as pd
from fastapi import FastAPI
from datetime import datetime, timedelta

from app.ml.train import train_model
from app.ml.model import create_model
from app.core.supabase import supabase
from app.data.fetch_data import fetch_gld_data
from app.data.features import compute_indicators

app = FastAPI()
MODEL_PATH = "models/gld_price_predictor.pkl"
FEATURE_COLUMNS = [
    "sma_20", "sma_50", "ema_20",
    "rsi", "macd", "macd_signal",
    "bb_upper", "bb_lower", "atr",
    "volume"
]

@app.on_event("startup")
def startup_event():
    print("🚀 Starting GoldIQ-Basic API...")

    os.makedirs("models", exist_ok=True)

    # 1️⃣ Fetch full GLD dataset
    print("⬇️ Fetching GLD data and computing indicators...")
    df = fetch_gld_data(start="2010-01-01")
    df = compute_indicators(df)
    print(df.head())

    # 2️⃣ Separate today's data (NO LEAKAGE)
    today_row = df.iloc[-1]
    train_df = df.iloc[:-1]

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df["close"]

    # 3️⃣ Initialize and train model
    model = create_model()
    version = datetime.utcnow().strftime("%Y%m%d_%H%M")

    metrics = train_model(model, X_train, y_train, version)

    # 4️⃣ Save model locally
    joblib.dump(model, MODEL_PATH)

    # 5️⃣ Predict today's price
    X_today = today_row[FEATURE_COLUMNS].values.reshape(1, -1)
    predicted_price = float(model.predict(X_today)[0])
    actual_price = float(today_row["close"])
    error = predicted_price - actual_price
    tomorrow_date = datetime.now() + timedelta(days=1)

    # 6️⃣ Store prediction in Supabase
    supabase.table("predictions").insert({
        "date_created": str(today_row["date"].date()),
        "actual_price": actual_price,
        "predicted_price": predicted_price,
        "error": error,
        "model_version": version,
         "prediction_for":str(tomorrow_date.strftime("%d-%m-%Y"))
    }).execute()

    # 7️⃣ Store model metrics in Supabase
    supabase.table("model_metrics").insert({
        "model_version": version,
        "rmse": metrics["rmse"],
        "mae": metrics["mae"],
        "mape": metrics["mape"],
        "r2": metrics["r2"],
        "training_samples": metrics["samples"],
        "trained_at": datetime.utcnow().isoformat()
    }).execute()

    print("✅ Model trained, prediction generated, and stored successfully.")

@app.get("/")
def predict_today():
    latest_prediction_response = supabase.table("predictions").select("*") \
    .order("date_created", desc=True).limit(1).execute()
    latest_prediction = latest_prediction_response.data[0]
    today = datetime.now().strftime("%d-%m-%Y")

    if latest_prediction["prediction_for"] == today:
        return {
            "latest_prediction": latest_prediction
        }
    else:
        return {
            "message": "Today's prediction is not available yet. Please check back later."
        }
    

