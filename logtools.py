import logging


def create_logger(log_name=__file__,
                  log_format="%(asctime)s %(levelname)8s %(name)s | %(message)s",
                  log_level=logging.ERROR):

    print(f"Creating logger with {log_name}")
    logger_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter(log_format)
    logger_handler.setFormatter(logger_formatter)
    
    logger = logging.getLogger(log_name)
    logger.addHandler(logger_handler)
    logger.setLevel(log_level)
    return logger
