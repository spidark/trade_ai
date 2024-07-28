import matplotlib.pyplot as plt

def plot_price_and_indicators(symbol, data, indicators):
    plt.figure(figsize=(14, 7))

    # Plot the closing price
    plt.plot(data[symbol]['Close'], label='Close Price')

    # Plot the Simple Moving Average (SMA)
    plt.plot(indicators[symbol]['SMA_20'], label='SMA 20')

    # Plot the Exponential Moving Average (EMA)
    plt.plot(indicators[symbol]['EMA_20'], label='EMA 20')

    # Plot the Bollinger Bands
    plt.plot(indicators[symbol]['Bollinger_Upper'], label='Bollinger Upper')
    plt.plot(indicators[symbol]['Bollinger_Middle'], label='Bollinger Middle')
    plt.plot(indicators[symbol]['Bollinger_Lower'], label='Bollinger Lower')

    # Plot the RSI
    plt.figure(figsize=(14, 4))
    plt.plot(indicators[symbol]['RSI_14'], label='RSI 14')
    plt.axhline(y=70, color='r', linestyle='-')
    plt.axhline(y=30, color='r', linestyle='-')

    # Adding the labels and title
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'Price and Technical Indicators for {symbol}')
    plt.legend()

    # Show the plot
    plt.show()
