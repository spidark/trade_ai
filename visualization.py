import matplotlib.pyplot as plt

def plot_price_and_indicators(symbol, data, indicators, output_dir):
    plt.figure(figsize=(14, 7))
    plt.plot(data[symbol]['Close'], label='Close Price')
    plt.plot(indicators[symbol]['SMA'], label='SMA')
    plt.plot(indicators[symbol]['EMA'], label='EMA')
    plt.plot(indicators[symbol]['RSI'], label='RSI')
    plt.title(f'{symbol} Price and Indicators')
    plt.legend()
    plt.savefig(f'{output_dir}/{symbol}_indicators.png')
    plt.close()

def plot_backtest_results(symbol, data, trading_log, output_dir):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    for log in trading_log:
        date, action, price, balance = log
        color = 'g' if action == 'buy' else 'r'
        plt.axvline(x=date, color=color, linestyle='--', alpha=0.7)
    plt.title(f'{symbol} Backtest Results')
    plt.legend()
    plt.savefig(f'{output_dir}/{symbol}_backtest.png')
    plt.close()
