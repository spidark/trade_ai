import os
import matplotlib.pyplot as plt

def plot_price_and_indicators(symbol, data, indicators, output_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price')
    for indicator_name, values in indicators.items():
        plt.plot(values, label=indicator_name)
    plt.title(f"{symbol} Price and Technical Indicators")
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{symbol}_price_and_indicators.png"))
    plt.close()

def plot_backtest_results(symbol, data, trading_log, output_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price')
    buy_signals = [log[2] for log in trading_log if log[1] == 'buy']
    buy_dates = [log[0] for log in trading_log if log[1] == 'buy']
    sell_signals = [log[2] for log in trading_log if log[1] == 'sell']
    sell_dates = [log[0] for log in trading_log if log[1] == 'sell']
    plt.plot(buy_dates, buy_signals, '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(sell_dates, sell_signals, 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title(f"{symbol} Backtest Results")
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{symbol}_backtest_results.png"))
    plt.close()

def plot_regression_results(X_test, y_test, y_pred, output_dir):
    plt.figure(figsize=(10, 6))
    plt.scatter(X_test.index, y_test, color='blue', label='Actual')
    plt.scatter(X_test.index, y_pred, color='red', label='Predicted')
    plt.xlabel('Index')
    plt.ylabel('Price')
    plt.title('Regression Model Results')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'regression_results.png'))
    plt.close()

def plot_clustering_results(data, clusters, output_dir):
    plt.figure(figsize=(10, 6))
    plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=clusters, cmap='viridis', marker='o')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Clustering Results')
    plt.savefig(os.path.join(output_dir, 'clustering_results.png'))
    plt.close()
