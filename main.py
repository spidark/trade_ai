import logging
import os
from data_fetcher import get_etf_symbols, get_cfd_symbols, get_forex_symbols, get_data
from movers_calculator import get_top_movers
from analyzer import analyze_data
from file_writer import write_to_file
from technical_indicators import add_technical_indicators  # Import ajouté
from visualization import plot_price_and_indicators

# Fichiers à supprimer
log_file = 'trade.log'
txt_file = 'trade.txt'

# Supprimer les fichiers s'ils existent
if os.path.exists(log_file):
    os.remove(log_file)
if os.path.exists(txt_file):
    os.remove(txt_file)

# Configuration de la journalisation
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
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
        
        # Analyser les données et ajouter les indicateurs techniques
        results = analyze_data(top_gainers_etf, top_losers_etf, etf_data, top_gainers_cfd, top_losers_cfd, cfd_data, top_gainers_forex, top_losers_forex, forex_data)
        
        # Écrire les résultats dans le fichier
        write_to_file('trade.txt', results)
        
        # Visualisation des données
        etf_indicators = add_technical_indicators(etf_data)
        for symbol in etf_symbols:
            plot_price_and_indicators(symbol, etf_data, etf_indicators)
        
        cfd_indicators = add_technical_indicators(cfd_data)
        for symbol in cfd_symbols:
            plot_price_and_indicators(symbol, cfd_data, cfd_indicators)
        
        forex_indicators = add_technical_indicators(forex_data)
        for symbol in forex_symbols:
            plot_price_and_indicators(symbol, forex_data, forex_indicators)

        logging.info('Script completed successfully')
    except Exception as e:
        logging.error(f'Error in main script: {e}')

if __name__ == "__main__":
    main()

print("Script completed successfully")
