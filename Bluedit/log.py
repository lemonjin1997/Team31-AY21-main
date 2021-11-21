import logging

formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


auth_logger_info = setup_logger('auth_logger', '../Log/authentication_log.txt', level=logging.INFO)
error_logger = setup_logger('error_logger', '../Log/error_log.txt', level=logging.ERROR)
post_logger = setup_logger('post_logger', '../Log/post_log.txt', level=logging.INFO)
user_logger = setup_logger('user_logger', '../Log/user_log.txt', level=logging.INFO)
admin_logger = setup_logger('admin_logger', '../Log/admin_log.txt', level=logging.INFO)