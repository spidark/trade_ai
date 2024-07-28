import pandas as pd

def estimate_max_profit(symbol, data):
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
