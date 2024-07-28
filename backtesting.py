import pandas as pd
import numpy as np
import logging

def backtest_strategy(data, symbol, strategy_func, initial_balance=10000):
    logging.info(f"Backtesting strategy for {symbol}")
    
    if 'Close' not in data.columns:
        logging.error(f"'Close' column not found in data for {symbol}")
        return None, []

    balance = initial_balance
    position = 0
    trading_log = []

    for i in range(1, len(data)):
        price = data['Close'].iloc[i]
        action = strategy_func(data.iloc[:i])
        
        if action == 'buy' and balance > price:
            # Buy one unit
            balance -= price
            position += 1
            trading_log.append((data.index[i], 'buy', price, balance))
        elif action == 'short' and position > 0:
            # Sell one unit
            balance += price
            position -= 1
            trading_log.append((data.index[i], 'sell', price, balance))
        
        # Log each action
        logging.debug(f"Date: {data.index[i]}, Action: {action}, Price: {price}, Balance: {balance}, Position: {position}")
    
    # Calculate final portfolio value
    final_value = balance + position * data['Close'].iloc[-1]
    logging.info(f"Final portfolio value for {symbol}: {final_value}")

    return final_value, trading_log

def simple_moving_average_strategy(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # Create short simple moving average
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()

    # Create long simple moving average
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Ensure the lengths match when assigning signals
    signals.loc[signals.index[short_window:], 'signal'] = np.where(
        signals.loc[signals.index[short_window:], 'short_mavg'] > signals.loc[signals.index[short_window:], 'long_mavg'], 1.0, 0.0
    )

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    def strategy_func(data):
        if len(signals) > 0:
            if signals['positions'].iloc[-1] == 1:
                return 'buy'
            elif signals['positions'].iloc[-1] == -1:
                return 'short'
            else:
                return 'hold'
        else:
            return 'hold'

    return strategy_func

def rsi_strategy(data, window=14, buy_threshold=30, sell_threshold=70):
    signals = pd.DataFrame(index=data.index)
    signals['RSI'] = calculate_rsi(data, window)

    def strategy_func(data):
        if signals['RSI'].iloc[-1] < buy_threshold:
            return 'buy'
        elif signals['RSI'].iloc[-1] > sell_threshold:
            return 'short'
        else:
            return 'hold'

    return strategy_func

def simple_strategy(data):
    """A simple strategy that buys if the close price is greater than the open price."""
    def strategy_func(data):
        if data['Close'].iloc[-1] > data['Open'].iloc[-1]:
            return 'buy'
        else:
            return 'hold'
    return strategy_func

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def write_backtest_log(symbol, trading_log, filename='backtest_log.txt'):
    try:
        with open(filename, 'a') as f:
            f.write(f"Backtesting results for {symbol}:\n")
            for log in trading_log:
                f.write(f"{log[0]}, {log[1]}, Price: {log[2]}, Balance: {log[3]}\n")
            f.write("\n")
        logging.info(f"Backtesting log written to {filename}")
    except Exception as e:
        logging.error(f"Error writing backtesting log: {e}")
