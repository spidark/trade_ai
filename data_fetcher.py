import logging
import yfinance as yf
import pandas as pd

def get_etf_symbols():
    logging.info('Fetching ETF symbols using yfinance')
    try:
        etf_symbols = ['MSS', 'SPY', 'IVV', 'VOO', 'QQQ', 'DIA', 'IWM', 'VNQ', 'GLD', 'XLK', 'EZU', 'MCHI', 'VGK', 'FXI', 'LIT', '^GDAXI']
        logging.info('ETF symbols fetched successfully')
        return etf_symbols
    except Exception as e:
        logging.error(f'Error fetching ETF symbols: {e}')
        return []

def get_cfd_symbols():
    logging.info('Fetching CFD symbols using yfinance')
    try:
        cfd_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NFLX', 'TSLA', 'BABA', 'NVDA', 
            'JPM', 'AMD', 'CME', 'INTC', 'META', 'BA', 'DIS', 'PYPL', 'CSCO', 
            'PEP', 'KO', 'NKE', 'WMT', 'PG', 'HD', 'VZ', 'T', 'XOM', 'CVX', 'MRK',
            'DJIA'
        ]
        logging.info('CFD symbols fetched successfully')
        return cfd_symbols
    except Exception as e:
        logging.error(f'Error fetching CFD symbols: {e}')
        return []

def get_forex_symbols():
    logging.info('Fetching Forex symbols using yfinance')
    try:
        forex_symbols = ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X']
        logging.info('Forex symbols fetched successfully')
        return forex_symbols
    except Exception as e:
        logging.error(f'Error fetching Forex symbols: {e}')
        return []

def get_data(symbols, period="1d", interval="5m"):
    logging.info(f'Fetching data for symbols using yfinance: {symbols}')
    try:
        data = yf.download(symbols, period=period, interval=interval, group_by='ticker')
        logging.info('Data fetched successfully')
        return data
    except Exception as e:
        logging.error(f'Error fetching data: {e}')
        return pd.DataFrame()
