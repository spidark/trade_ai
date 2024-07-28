import pandas as pd

def add_technical_indicators(data):
    short_window = 40
    long_window = 100
    data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    data['rsi'] = calculate_rsi(data['Close'])
    return data

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def add_multitemp_indicators(data):
    windows = [5, 10, 20]  # Short, medium, long term windows
    for window in windows:
        data[f'SMA_{window}'] = calculate_moving_average(data, window)
        data[f'RSI_{window}'] = calculate_rsi(data['Close'], window)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()
