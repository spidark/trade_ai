import pandas as pd

def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data, window):
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    sma = data['Close'].rolling(window=window).mean()
    std_dev = data['Close'].rolling(window=window).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return upper_band, sma, lower_band

def calculate_average_volume(data, window):
    return data['Volume'].rolling(window=window).mean()

def add_technical_indicators(data):
    indicators = {}
    for symbol in data.columns.levels[0]:
        indicators[symbol] = {
            'SMA_20': calculate_sma(data[symbol], 20),
            'EMA_20': calculate_ema(data[symbol], 20),
            'RSI_14': calculate_rsi(data[symbol]),
            'Bollinger_Upper': calculate_bollinger_bands(data[symbol])[0],
            'Bollinger_Middle': calculate_bollinger_bands(data[symbol])[1],
            'Bollinger_Lower': calculate_bollinger_bands(data[symbol])[2],
            'Average_Volume_20': calculate_average_volume(data[symbol], 20)
        }
    return indicators
