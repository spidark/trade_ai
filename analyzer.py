import logging
import pandas as pd

def analyze_movement(percent_change):
    if percent_change > 2:
        return "buy"
    elif percent_change < -2:
        return "short"
    else:
        return "hold"

def estimate_max_profit(symbol, data):
    data[symbol].loc[:, 'Close'] = data[symbol]['Close'].ffill().bfill()  # Remplir les valeurs NA correctement
    recent_data = data[symbol]['Close']
    max_profit = (recent_data.max() - recent_data.min()) / recent_data.min() * 100
    return max_profit

def calculate_tp(symbol, data, action):
    recent_close = data[symbol]['Close'].iloc[-1]
    if action == "buy":
        tp = recent_close * 1.02
    elif action == "short":
        tp = recent_close * 0.98
    else:
        tp = recent_close
    return tp

def estimate_duration(symbol, data, action):
    data[symbol].loc[:, 'Close'] = data[symbol]['Close'].ffill().bfill()  # Remplir les valeurs NA correctement
    recent_close = data[symbol]['Close'].iloc[-1]
    tp = calculate_tp(symbol, data, action)
    if action == "buy":
        movement = data[symbol]['Close'].pct_change().mean()
        duration = abs(tp - recent_close) / (recent_close * movement) if movement != 0 else float('inf')
    elif action == "short":
        movement = -data[symbol]['Close'].pct_change().mean()
        duration = abs(tp - recent_close) / (recent_close * movement) if movement != 0 else float('inf')
    else:
        duration = 0
    return duration

def add_technical_indicators(data):
    data['SMA'] = data['Close'].rolling(window=20).mean()
    data['EMA'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['RSI'] = calculate_rsi(data['Close'])
    data['Upper_BB'], data['Lower_BB'] = calculate_bollinger_bands(data['Close'])
    data = add_multitemp_indicators(data)
    return data

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(close, window=20):
    sma = close.rolling(window).mean()
    std = close.rolling(window).std()
    upper_bb = sma + (std * 2)
    lower_bb = sma - (std * 2)
    return upper_bb, lower_bb

def add_multitemp_indicators(data):
    windows = [5, 10, 20]  # Short, medium, long term windows
    for window in windows:
        data[f'SMA_{window}'] = calculate_moving_average(data, window)
        data[f'RSI_{window}'] = calculate_rsi(data['Close'], window)
    return data

def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

def analyze_data(top_gainers_etf, top_losers_etf, etf_data, top_gainers_cfd, top_losers_cfd, cfd_data, top_gainers_forex, top_losers_forex, forex_data):
    results = []
    for item in top_gainers_etf:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], etf_data)
        tp = calculate_tp(item[0], etf_data, action)
        duration = estimate_duration(item[0], etf_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    for item in top_losers_etf:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], etf_data)
        tp = calculate_tp(item[0], etf_data, action)
        duration = estimate_duration(item[0], etf_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    for item in top_gainers_cfd:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], cfd_data)
        tp = calculate_tp(item[0], cfd_data, action)
        duration = estimate_duration(item[0], cfd_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    for item in top_losers_cfd:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], cfd_data)
        tp = calculate_tp(item[0], cfd_data, action)
        duration = estimate_duration(item[0], cfd_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    for item in top_gainers_forex:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], forex_data)
        tp = calculate_tp(item[0], forex_data, action)
        duration = estimate_duration(item[0], forex_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    for item in top_losers_forex:
        action = analyze_movement(float(item[1]))
        max_profit = estimate_max_profit(item[0], forex_data)
        tp = calculate_tp(item[0], forex_data, action)
        duration = estimate_duration(item[0], forex_data, action)
        results.append((item[0], item[1], action, tp, max_profit, duration))
    return results
