import joblib
# import pandas as pd
from fastapi import FastAPI
# from datetime import datetime

from app.ml.train import train_model
from app.ml.model import create_model
from app.core.supabase import supabase
from app.data.fetch_data import fetch_gld_data
from app.data.features import compute_indicators

app = FastAPI()
MODEL_PATH = "models/gld_price_predictor.pkl"

@app.on_event("startup")
def startup_event():
    print("Starting GoldIQ-Basic API...")
    try:
        model = joblib.load(MODEL_PATH)
        if model:
            print("Model loaded successfully.")
    except Exception as e: #noqa
        print("No model found, training the model...")

    df = fetch_gld_data(start="2022-01-01")
    df = compute_indicators(df)
    latest = df.iloc[-1]

    model = create_model()

    X = df.drop(columns=["Date", "Close"])
    y = df["Close"]

    predictions = train_model(model, X, y, version="latest")
    

@app.get("/")
def predict_today():
    model = joblib.load(MODEL_PATH)

    df = fetch_gld_data(start="2024-01-01")
    df = compute_indicators(df)

    latest = df.iloc[-1]
    X = latest.drop(["Date", "Close"])

    prediction = model.predict([X])[0]

    supabase.table("predictions").insert({
        "date": str(latest["Date"].date()),
        "actual_price": float(latest["Close"]),
        "predicted_price": float(prediction),
        "error": float(prediction - latest["Close"]),
        "model_version": "latest"
    }).execute()

    return {
        "date": latest["Date"],
        "actual": latest["Close"],
        "prediction": prediction
    }
