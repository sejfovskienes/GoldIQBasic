# import pandas as pd 
# import numpy as np 

def compute_indicators(df):
    df["sma_20"] = df["Close"].rolling(20).mean()
    df["sma_50"] = df["Close"].rolling(50).mean()
    df["ema_20"] = df["Close"].ewm(span=20).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100 / (1 + rs))

    df["macd"] = df["ema_20"] - df["Close"].ewm(span=26).mean()
    df["macd_signal"] = df["macd"].ewm(span=9).mean()

    df["bb_upper"] = df["sma_20"] + 2 * df["Close"].rolling(20).std()
    df["bb_lower"] = df["sma_20"] - 2 * df["Close"].rolling(20).std()

    df["atr"] = (df["High"] - df["Low"]).rolling(14).mean()

    return df.dropna()
