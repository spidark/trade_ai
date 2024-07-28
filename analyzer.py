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
    if symbol not in data or 'Close' not in data[symbol].columns:
        logging.error(f'Cannot estimate max profit for {symbol}: Missing data or Close column')
        return 0
    recent_data = data[symbol]['Close']
    max_profit = (recent_data.max() - recent_data.min()) / recent_data.min() * 100
    return max_profit

def calculate_tp(symbol, data, action):
    if symbol not in data or 'Close' not in data[symbol].columns:
        logging.error(f'Cannot calculate TP for {symbol}: Missing data or Close column')
        return 0
    recent_close = data[symbol]['Close'].iloc[-1]
    if action == "buy":
        tp = recent_close * 1.02
    elif action == "short":
        tp = recent_close * 0.98
    else:
        tp = recent_close
    return tp

def estimate_duration(symbol, data, action):
    if symbol not in data or 'Close' not in data[symbol].columns:
        logging.error(f'Cannot estimate duration for {symbol}: Missing data or Close column')
        return 0
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

def analyze_data(top_gainers_etf, top_losers_etf, etf_data, top_gainers_cfd, top_losers_cfd, cfd_data, top_gainers_forex, top_losers_forex, forex_data):
    results = []
    logging.info("Analyzing ETF data")
    for item in top_gainers_etf + top_losers_etf:
        symbol = item[0]
        if symbol in etf_data and 'Close' in etf_data[symbol].columns:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(symbol, etf_data)
            tp = calculate_tp(symbol, etf_data, action)
            duration = estimate_duration(symbol, etf_data, action)
            results.append((symbol, item[1], action, tp, max_profit, duration))
        else:
            logging.error(f'Missing Close data for ETF: {symbol}')
    
    logging.info("Analyzing CFD data")
    for item in top_gainers_cfd + top_losers_cfd:
        symbol = item[0]
        if symbol in cfd_data and 'Close' in cfd_data[symbol].columns:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(symbol, cfd_data)
            tp = calculate_tp(symbol, cfd_data, action)
            duration = estimate_duration(symbol, cfd_data, action)
            results.append((symbol, item[1], action, tp, max_profit, duration))
        else:
            logging.error(f'Missing Close data for CFD: {symbol}')
    
    logging.info("Analyzing Forex data")
    for item in top_gainers_forex + top_losers_forex:
        symbol = item[0]
        if symbol in forex_data and 'Close' in forex_data[symbol].columns:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(symbol, forex_data)
            tp = calculate_tp(symbol, forex_data, action)
            duration = estimate_duration(symbol, forex_data, action)
            results.append((symbol, item[1], action, tp, max_profit, duration))
        else:
            logging.error(f'Missing Close data for Forex: {symbol}')
    
    return results
