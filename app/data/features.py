# import pandas as pd 
# import numpy as np 

def compute_indicators(df):
    # Moving averages
    df["sma_20"] = df["close"].rolling(20).mean()
    df["sma_50"] = df["close"].rolling(50).mean()

    df["ema_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["ema_26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # MACD
    df["macd"] = df["ema_12"] - df["ema_26"]
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df["rsi"] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    rolling_std = df["close"].rolling(20).std()
    df["bb_upper"] = df["sma_20"] + 2 * rolling_std
    df["bb_lower"] = df["sma_20"] - 2 * rolling_std

    # ATR
    df["atr"] = (df["high"] - df["low"]).rolling(14).mean()

    return df.dropna()
