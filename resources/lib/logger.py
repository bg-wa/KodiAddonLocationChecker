import logging


def setup_logging():
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    log_level = logging.DEBUG

    # Create a logger object
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create a console handler and set its level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create a file handler, set its level and formatter
    file_handler = logging.FileHandler('application.log')
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # With this setup, log messages will be output to both the console and a file named 'application.log'
