import pandas as pd

def add_technical_indicators(data):
    short_window = 40
    long_window = 100
    data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    data['rsi'] = calculate_rsi(data['Close'])
    data['macd'], data['signal_line'] = calculate_macd(data['Close'])
    data['bollinger_upper'], data['bollinger_lower'] = calculate_bollinger_bands(data['Close'])
    return data

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, short_period=12, long_period=26, signal_period=9):
    short_ema = series.ewm(span=short_period, adjust=False).mean()
    long_ema = series.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line

def calculate_bollinger_bands(series, window=20):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return upper_band, lower_band

def add_multitemp_indicators(data):
    windows = [5, 10, 20]  # Short, medium, long term windows
    for window in windows:
        data[f'SMA_{window}'] = calculate_moving_average(data, window)
        data[f'RSI_{window}'] = calculate_rsi(data['Close'], window)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()
