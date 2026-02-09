import yfinance as yf

def fetch_gld_data(start="2010-01-01"):
    df = yf.download("GLD", start=start)

    df = df.reset_index()
    df.columns = [col.lower() if isinstance(col, str) else col[0].lower() for col in df.columns]

    return df