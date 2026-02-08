import yfinance as yf

def fetch_gld_data(start="2010-01-01"):
    gld = yf.download("GLD", start=start)
    gld.reset_index(inplace=True)
    return gld