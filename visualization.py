import logging
import matplotlib.pyplot as plt
import os

def plot_price_and_indicators(symbol, data, indicators, output_dir):
    try:
        plt.figure(figsize=(14, 7))
        logging.debug(f"Data for plotting: {data[symbol].head()}")
        plt.plot(data[symbol].index, data[symbol]['Close'], label='Close Price', color='blue')
        
        # Plot SMA and EMA
        if 'SMA' in indicators:
            plt.plot(indicators.index, indicators['SMA'], label='SMA', color='orange')
        if 'EMA' in indicators:
            plt.plot(indicators.index, indicators['EMA'], label='EMA', color='green')
        
        plt.title(f'Price and Indicators for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        
        plt.savefig(os.path.join(output_dir, f'{symbol}_price_indicators.png'))
        plt.close()

        # Plot RSI
        if 'RSI' in indicators:
            plt.figure(figsize=(14, 4))
            plt.plot(indicators.index, indicators['RSI'], label='RSI', color='purple')
            plt.axhline(y=70, color='r', linestyle='-')
            plt.axhline(y=30, color='g', linestyle='-')
            plt.title(f'RSI for {symbol}')
            plt.xlabel('Date')
            plt.ylabel('RSI')
            plt.legend()
            plt.grid()
            
            plt.savefig(os.path.join(output_dir, f'{symbol}_RSI.png'))
            plt.close()
    except Exception as e:
        logging.error(f"Error plotting price and indicators for {symbol}: {e}")

def plot_backtest_results(symbol, data, trading_log, output_dir):
    try:
        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        
        # Plot buy signals
        buys = [(log[0], log[2]) for log in trading_log if log[1] == 'buy']
        if buys:
            buy_dates, buy_prices = zip(*buys)
            plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy Signal', alpha=1)
        
        # Plot sell signals
        sells = [(log[0], log[2]) for log in trading_log if log[1] == 'sell']
        if sells:
            sell_dates, sell_prices = zip(*sells)
            plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell Signal', alpha=1)
        
        plt.title(f'Backtesting Results for {symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        
        plt.savefig(os.path.join(output_dir, f'{symbol}_backtest.png'))
        plt.close()
    except Exception as e:
        logging.error(f"Error plotting backtest results for {symbol}: {e}")
