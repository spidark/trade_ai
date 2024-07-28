import pandas as pd

def add_technical_indicators(data):
    data['SMA'] = data['Close'].rolling(window=14).mean()
    data['EMA'] = data['Close'].ewm(span=14, adjust=False).mean()
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    data['RSI'] = 100 - (100 / (1 + RS))
    return data
