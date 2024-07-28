import logging
import pandas as pd

def get_top_movers(data):
    logging.info('Calculating top movers')
    try:
        movers = {}
        for symbol in data.columns.levels[0]:
            if 'Close' in data[symbol] and 'Open' in data[symbol]:
                latest_price = data[symbol]['Close'].iloc[-1]
                opening_price = data[symbol]['Open'].iloc[0]
                if pd.isna(latest_price) or pd.isna(opening_price):
                    continue
                percent_change = ((latest_price - opening_price) / opening_price) * 100
                movers[symbol] = percent_change
        sorted_movers = sorted(movers.items(), key=lambda x: x[1])
        top_gainers = sorted_movers[-5:]
        top_losers = sorted_movers[:5]
        logging.info('Top movers calculated successfully')
        return top_gainers, top_losers
    except Exception as e:
        logging.error(f'Error calculating top movers: {e}')
        return [], []