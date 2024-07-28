import logging
import os
from data_fetcher import get_etf_symbols, get_cfd_symbols, get_forex_symbols, get_data
from movers_calculator import get_top_movers
from analyzer import analyze_movement, estimate_max_profit, calculate_tp, estimate_duration
from file_writer import write_to_file

# Fichiers à supprimer
log_file = 'trade.log'
txt_file = 'trade.txt'

# Supprimer les fichiers s'ils existent
if os.path.exists(log_file):
    os.remove(log_file)
if os.path.exists(txt_file):
    os.remove(txt_file)

# Configuration de la journalisation
logging.basicConfig(filename='trade.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def main():
    logging.info('Starting main script')
    try:
        # Récupérer les symboles et les données pour les ETF
        etf_symbols = get_etf_symbols()
        etf_data = get_data(etf_symbols, period="5d", interval="1d")
        top_gainers_etf, top_losers_etf = get_top_movers(etf_data)
        
        # Récupérer les symboles et les données pour les CFD
        cfd_symbols = get_cfd_symbols()
        cfd_data = get_data(cfd_symbols, period="1d", interval="1m")
        top_gainers_cfd, top_losers_cfd = get_top_movers(cfd_data)
        
        # Journalisation pour CFD
        logging.debug(f'CFD Data: {cfd_data}')
        logging.debug(f'Top Gainers CFDs: {top_gainers_cfd}')
        logging.debug(f'Top Losers CFDs: {top_losers_cfd}')

        # Récupérer les symboles et les données pour les paires Forex
        forex_symbols = get_forex_symbols()
        forex_data = get_data(forex_symbols, period="1mo", interval="1d")
        top_gainers_forex, top_losers_forex = get_top_movers(forex_data)
        
        # Préparer les résultats
        lines = []
        lines.append("Top 5 Gainers ETFs (5 Days):\n")
        for item in top_gainers_etf:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], etf_data)
            tp = calculate_tp(item[0], etf_data, action)
            duration = estimate_duration(item[0], etf_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        lines.append("\nTop 5 Losers ETFs (5 Days):\n")
        for item in top_losers_etf:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], etf_data)
            tp = calculate_tp(item[0], etf_data, action)
            duration = estimate_duration(item[0], etf_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        lines.append("\nTop 5 Gainers CFDs (Last Day):\n")
        for item in top_gainers_cfd:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], cfd_data)
            tp = calculate_tp(item[0], cfd_data, action)
            duration = estimate_duration(item[0], cfd_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        lines.append("\nTop 5 Losers CFDs (Last Day):\n")
        for item in top_losers_cfd:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], cfd_data)
            tp = calculate_tp(item[0], cfd_data, action)
            duration = estimate_duration(item[0], cfd_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        lines.append("\nTop 5 Gainers Forex Pairs (Last Day):\n")
        for item in top_gainers_forex:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], forex_data)
            tp = calculate_tp(item[0], forex_data, action)
            duration = estimate_duration(item[0], forex_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        lines.append("\nTop 5 Losers Forex Pairs (Last Day):\n")
        for item in top_losers_forex:
            action = analyze_movement(item[1])
            max_profit = estimate_max_profit(item[0], forex_data)
            tp = calculate_tp(item[0], forex_data, action)
            duration = estimate_duration(item[0], forex_data, action)
            line = f"{item[0]}: {item[1]:.2f}%, Action: {action}, TP: {tp:.2f}, Max Profit: {max_profit:.2f}%, Duration: {duration:.2f} hours\n"
            lines.append(line)
        
        # Écrire les résultats dans le fichier
        write_to_file('trade.txt', lines)
        logging.info('Script completed successfully')
    except Exception as e:
        logging.error(f'Error in main script: {e}')

if __name__ == "__main__":
    main()

print("Script completed successfully")
