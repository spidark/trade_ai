import logging

def write_to_file(filename, lines):
    logging.info(f'Writing results to file: {filename}')
    try:
        with open(filename, 'w') as file:
            for line in lines:
                file.write(line)
                logging.debug(f'Writing line: {line.strip()}')
        logging.info('Results successfully written to file')
    except Exception as e:
        logging.error(f'Error writing to file: {e}')
