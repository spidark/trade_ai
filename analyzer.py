import logging

def analyze_movement(percent_change):
    logging.debug(f'Analyzing movement: {percent_change}')
    if percent_change > 1:
        return "buy"
    elif percent_change < -1:
        return "short"
    else:
        return "hold"

def estimate_max_profit(symbol, data):
    try:
        prices = data[symbol]['Close']
        max_profit = (prices.max() - prices.min()) / prices.min() * 100
        return max_profit
    except Exception as e:
        logging.error(f'Error estimating max profit for {symbol}: {e}')
        return 0

def calculate_tp(symbol, data, action):
    try:
        opening_price = data[symbol]['Open'].iloc[0]
        if action == "buy":
            tp = opening_price * 1.05  # 5% au-dessus du prix d'ouverture
        elif action == "short":
            tp = opening_price * 0.95  # 5% en-dessous du prix d'ouverture
        else:
            tp = opening_price
        return tp
    except Exception as e:
        logging.error(f'Error calculating TP for {symbol}: {e}')
        return 0
