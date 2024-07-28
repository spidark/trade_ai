import logging
import pandas as pd
import numpy as np

def simple_moving_average_strategy(data, short_window=40, long_window=100):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    signals['signal'][short_window:] = np.where(
        signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0
    )

    signals['positions'] = signals['signal'].diff()

    return signals

def backtest_strategy(data, symbol, signals, initial_balance=10000.0):
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions[symbol] = signals['signal']
    portfolio = positions.multiply(data['Close'], axis=0)
    pos_diff = positions.diff()
    portfolio['holdings'] = (positions.multiply(data['Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_balance - (pos_diff.multiply(data['Close'], axis=0)).sum(axis=1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    trading_log = []

    for date in portfolio.index:
        if signals['positions'].loc[date] == 1.0:
            trading_log.append((date, 'buy', data['Close'].loc[date], portfolio['total'].loc[date]))
        elif signals['positions'].loc[date] == -1.0:
            trading_log.append((date, 'sell', data['Close'].loc[date], portfolio['total'].loc[date]))

    return portfolio['total'].iloc[-1], trading_log

def simple_strategy(data):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals['signal'][10:] = np.where(data['Close'][10:] > data['Close'].shift(1)[10:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals

def rsi_strategy(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    RS = gain / loss
    data['RSI'] = 100 - (100 / (1 + RS))
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    signals['signal'][window:] = np.where(data['RSI'][window:] > 70, -1.0, np.where(data['RSI'][window:] < 30, 1.0, 0.0))
    signals['positions'] = signals['signal'].diff()
    return signals

def write_backtest_log(symbol, trading_log, log_file):
    try:
        with open(log_file, 'a') as file:
            file.write(f'Backtesting results for {symbol}:\n')
            for log in trading_log:
                file.write(f'{log[0]}, {log[1]}, Price: {log[2]}, Balance: {log[3]}\n')
        logging.info(f'Backtesting log successfully written to file: {log_file}')
    except Exception as e:
        logging.error(f'Error writing backtesting log to file: {e}')
