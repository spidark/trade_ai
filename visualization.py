import os
import matplotlib.pyplot as plt

def plot_price_and_indicators(symbol, data, indicators, output_dir):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    for key, value in indicators.items():
        plt.plot(value, label=key)
    plt.title(f'Price and Technical Indicators for {symbol}')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{symbol}_price_indicators.png'))
    plt.close()

def plot_backtest_results(symbol, data, trading_log, output_dir):
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    buy_signals = [log for log in trading_log if log[1] == 'buy']
    sell_signals = [log for log in trading_log if log[1] == 'sell']
    plt.scatter([log[0] for log in buy_signals], [log[2] for log in buy_signals], marker='^', color='g', label='Buy Signal', alpha=1)
    plt.scatter([log[0] for log in sell_signals], [log[2] for log in sell_signals], marker='v', color='r', label='Sell Signal', alpha=1)
    plt.title(f'Backtest Results for {symbol}')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f'{symbol}_backtest.png'))
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
