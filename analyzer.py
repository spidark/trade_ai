import logging
from movement_analysis import analyze_movement
from profit_estimation import estimate_max_profit, calculate_tp, estimate_duration
from technical_indicators import add_technical_indicators

def analyze_data(top_gainers_etf, top_losers_etf, etf_data, top_gainers_cfd, top_losers_cfd, cfd_data, top_gainers_forex, top_losers_forex, forex_data):
    results = []

    results.append("Top 5 Gainers ETFs (5 Days):\n")
    etf_indicators = add_technical_indicators(etf_data)
    for item in top_gainers_etf:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], etf_data)
        tp = calculate_tp(item[0], etf_data, action)
        duration = estimate_duration(item[0], etf_data, action)
        indicators = etf_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    results.append("\nTop 5 Losers ETFs (5 Days):\n")
    for item in top_losers_etf:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], etf_data)
        tp = calculate_tp(item[0], etf_data, action)
        duration = estimate_duration(item[0], etf_data, action)
        indicators = etf_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    results.append("\nTop 5 Gainers CFDs (Last Day):\n")
    cfd_indicators = add_technical_indicators(cfd_data)
    for item in top_gainers_cfd:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], cfd_data)
        tp = calculate_tp(item[0], cfd_data, action)
        duration = estimate_duration(item[0], cfd_data, action)
        indicators = cfd_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    results.append("\nTop 5 Losers CFDs (Last Day):\n")
    for item in top_losers_cfd:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], cfd_data)
        tp = calculate_tp(item[0], cfd_data, action)
        duration = estimate_duration(item[0], cfd_data, action)
        indicators = cfd_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    results.append("\nTop 5 Gainers Forex Pairs (Last Day):\n")
    forex_indicators = add_technical_indicators(forex_data)
    for item in top_gainers_forex:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], forex_data)
        tp = calculate_tp(item[0], forex_data, action)
        duration = estimate_duration(item[0], forex_data, action)
        indicators = forex_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    results.append("\nTop 5 Losers Forex Pairs (Last Day):\n")
    for item in top_losers_forex:
        action = analyze_movement(item[1])
        max_profit = estimate_max_profit(item[0], forex_data)
        tp = calculate_tp(item[0], forex_data, action)
        duration = estimate_duration(item[0], forex_data, action)
        indicators = forex_indicators[item[0]]
        line = (f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, "
                f"Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours, "
                f"SMA_20: {indicators['SMA_20'].iloc[-1]:.2f}, EMA_20: {indicators['EMA_20'].iloc[-1]:.2f}, "
                f"RSI_14: {indicators['RSI_14'].iloc[-1]:.2f}, Bollinger_Upper: {indicators['Bollinger_Upper'].iloc[-1]:.2f}, "
                f"Bollinger_Middle: {indicators['Bollinger_Middle'].iloc[-1]:.2f}, Bollinger_Lower: {indicators['Bollinger_Lower'].iloc[-1]:.2f}, "
                f"Average_Volume_20: {indicators['Average_Volume_20'].iloc[-1]:.2f}\n")
        results.append(line)

    return results
