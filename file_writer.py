import logging

def write_to_file(filename, lines):
    try:
        with open(filename, 'w') as file:
            file.writelines(lines)
        logging.info(f'Results successfully written to file: {filename}')
    except Exception as e:
        logging.error(f'Error writing to file: {e}')
