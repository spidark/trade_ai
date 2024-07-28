import logging
import csv

def write_to_csv(filename, lines):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
        logging.info(f'Results successfully written to file: {filename}')
    except Exception as e:
        logging.error(f'Error writing to file: {e}')
