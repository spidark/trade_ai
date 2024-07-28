import logging
import os
from data_fetcher import get_etf_symbols, get_cfd_symbols, get_forex_symbols, get_data
from movers_calculator import get_top_movers
from analyzer import analyze_data, analyze_movement, estimate_max_profit, calculate_tp
from file_writer import write_to_csv
from technical_indicators import add_technical_indicators
from visualization import plot_price_and_indicators, plot_backtest_results
from backtesting import backtest_strategy, simple_moving_average_strategy, simple_strategy, rsi_strategy, write_backtest_log
from machine_learning import train_regression_model, predict_price, train_clustering_model, cluster_data

# Fichiers à supprimer
log_file = 'trade.log'
csv_file = 'trade.csv'
backtest_log_file = 'backtest_log.txt'

# Supprimer les fichiers s'ils existent
if os.path.exists(log_file):
    os.remove(log_file)
if os.path.exists(csv_file):
    os.remove(csv_file)
if os.path.exists(backtest_log_file):
    os.remove(backtest_log_file)

# Créer le répertoire de sortie pour les graphiques
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configuration de la journalisation
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def check_close_column(data, symbols):
    missing_close = []
    for symbol in symbols:
        if symbol in data and 'Close' in data[symbol].columns:
            logging.debug(f"Column 'Close' found in data for symbol: {symbol}")
        else:
            logging.error(f"Column 'Close' not found in data for symbol: {symbol}")
            missing_close.append(symbol)
    return missing_close

def main():
    logging.info('Starting main script')
    try:
        # Récupérer les symboles et les données pour les ETF
        etf_symbols = get_etf_symbols()
        etf_data = get_data(etf_symbols, period="5d", interval="1d")
        logging.debug(f'ETF Data: {etf_data.head()}')
        top_gainers_etf, top_losers_etf = get_top_movers(etf_data)
        missing_close_etf = check_close_column(etf_data, etf_symbols)
        if missing_close_etf:
            raise ValueError(f"Column 'Close' not found in ETF data for symbols: {missing_close_etf}")

        # Récupérer les symboles et les données pour les CFD
        cfd_symbols = get_cfd_symbols()
        cfd_data = get_data(cfd_symbols, period="1d", interval="1m")
        logging.debug(f'CFD Data: {cfd_data.head()}')
        top_gainers_cfd, top_losers_cfd = get_top_movers(cfd_data)
        missing_close_cfd = check_close_column(cfd_data, cfd_symbols)
        if missing_close_cfd:
            raise ValueError(f"Column 'Close' not found in CFD data for symbols: {missing_close_cfd}")

        # Journalisation pour CFD
        logging.debug(f'Top Gainers CFDs: {top_gainers_cfd}')
        logging.debug(f'Top Losers CFDs: {top_losers_cfd}')

        # Récupérer les symboles et les données pour les paires Forex
        forex_symbols = get_forex_symbols()
        forex_data = get_data(forex_symbols, period="1mo", interval="1d")
        logging.debug(f'Forex Data: {forex_data.head()}')
        top_gainers_forex, top_losers_forex = get_top_movers(forex_data)
        missing_close_forex = check_close_column(forex_data, forex_symbols)
        if missing_close_forex:
            raise ValueError(f"Column 'Close' not found in Forex data for symbols: {missing_close_forex}")

        # Analyser les données et ajouter les indicateurs techniques
        logging.info("Analyzing data and adding technical indicators")
        results = analyze_data(top_gainers_etf, top_losers_etf, etf_data, top_gainers_cfd, top_losers_cfd, cfd_data, top_gainers_forex, top_losers_forex, forex_data)
        
        # Préparer les résultats au format CSV
        csv_lines = [["Category", "Symbol", "Percent Change", "Action", "TP", "Max Profit"]]
        csv_lines += [["Top Gainers ETFs (5 Days)"]]
        for item in top_gainers_etf:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], etf_data)
            tp = calculate_tp(item[0], etf_data, action)
            csv_lines.append(["ETF Gainers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])
        
        csv_lines += [["Top Losers ETFs (5 Days)"]]
        for item in top_losers_etf:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], etf_data)
            tp = calculate_tp(item[0], etf_data, action)
            csv_lines.append(["ETF Losers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])
        
        csv_lines += [["Top Gainers CFDs (Last Day)"]]
        for item in top_gainers_cfd:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], cfd_data)
            tp = calculate_tp(item[0], cfd_data, action)
            csv_lines.append(["CFD Gainers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])
        
        csv_lines += [["Top Losers CFDs (Last Day)"]]
        for item in top_losers_cfd:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], cfd_data)
            tp = calculate_tp(item[0], cfd_data, action)
            csv_lines.append(["CFD Losers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])
        
        csv_lines += [["Top Gainers Forex Pairs (Last Day)"]]
        for item in top_gainers_forex:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], forex_data)
            tp = calculate_tp(item[0], forex_data, action)
            csv_lines.append(["Forex Gainers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])
        
        csv_lines += [["Top Losers Forex Pairs (Last Day)"]]
        for item in top_losers_forex:
            action = analyze_movement(float(item[1]))
            max_profit = estimate_max_profit(item[0], forex_data)
            tp = calculate_tp(item[0], forex_data, action)
            csv_lines.append(["Forex Losers", item[0], f"{item[1]:.2f}%", action, f"{tp:.2f}", f"{max_profit:.2f}%"])

        # Écrire les résultats dans le fichier CSV
        write_to_csv('trade.csv', csv_lines)
        
        # Visualisation des données pour les top gainers et losers
        logging.info("Adding technical indicators for ETF data")
        etf_indicators = add_technical_indicators(etf_data)
        for symbol, _ in top_gainers_etf + top_losers_etf:
            logging.info(f"Plotting price and indicators for ETF: {symbol}")
            if symbol in etf_data and 'Close' in etf_data[symbol].columns:
                plot_price_and_indicators(symbol, etf_data[symbol], etf_indicators, output_dir)
            else:
                logging.error(f"Column 'Close' not found in ETF data for symbol: {symbol}")
        
        logging.info("Adding technical indicators for CFD data")
        cfd_indicators = add_technical_indicators(cfd_data)
        for symbol, _ in top_gainers_cfd + top_losers_cfd:
            logging.info(f"Plotting price and indicators for CFD: {symbol}")
            if symbol in cfd_data and 'Close' in cfd_data[symbol].columns:
                plot_price_and_indicators(symbol, cfd_data[symbol], cfd_indicators, output_dir)
            else:
                logging.error(f"Column 'Close' not found in CFD data for symbol: {symbol}")
        
        logging.info("Adding technical indicators for Forex data")
        forex_indicators = add_technical_indicators(forex_data)
        for symbol, _ in top_gainers_forex + top_losers_forex:
            logging.info(f"Plotting price and indicators for Forex: {symbol}")
            if symbol in forex_data and 'Close' in forex_data[symbol].columns:
                plot_price_and_indicators(symbol, forex_data[symbol], forex_indicators, output_dir)
            else:
                logging.error(f"Column 'Close' not found in Forex data for symbol: {symbol}")

        # Backtesting des stratégies de trading
        for symbol in etf_symbols:
            logging.debug(f"Data for {symbol}: {etf_data[symbol].head()}")
            strategy = simple_moving_average_strategy(etf_data[symbol])
            final_value, trading_log = backtest_strategy(etf_data[symbol], symbol, strategy)
            logging.info(f"Backtesting {symbol}: Final portfolio value: {final_value}")
            write_backtest_log(symbol, trading_log, backtest_log_file)
            plot_backtest_results(symbol, etf_data[symbol], trading_log, output_dir)
            
            # Test with simple strategy
            simple_strat = simple_strategy(etf_data[symbol])
            final_value, trading_log = backtest_strategy(etf_data[symbol], symbol, simple_strat)
            logging.info(f"Backtesting with simple strategy {symbol}: Final portfolio value: {final_value}")
            write_backtest_log(f"{symbol}_simple_strategy", trading_log, backtest_log_file)
            plot_backtest_results(f"{symbol}_simple_strategy", etf_data[symbol], trading_log, output_dir)

            # Test with RSI strategy
            rsi_strat = rsi_strategy(etf_data[symbol])
            final_value, trading_log = backtest_strategy(etf_data[symbol], symbol, rsi_strat)
            logging.info(f"Backtesting with RSI strategy {symbol}: Final portfolio value: {final_value}")
            write_backtest_log(f"{symbol}_rsi_strategy", trading_log, backtest_log_file)
            plot_backtest_results(f"{symbol}_rsi_strategy", etf_data[symbol], trading_log, output_dir)
        
        logging.info('Script completed successfully')
    except Exception as e:
        logging.error(f'Error in main script: {e}', exc_info=True)

if __name__ == "__main__":
    main()

print("Script completed successfully")
