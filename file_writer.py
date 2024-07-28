import logging
import csv

def write_to_csv(filename, data):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Symbol", "Percent Change", "Action", "TP", "Max Profit"])
            for row in data:
                writer.writerow(row)
        logging.info(f'Results successfully written to CSV file: {filename}')
    except Exception as e:
        logging.error(f'Error writing to CSV file: {e}')
