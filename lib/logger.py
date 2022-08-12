import logging
import colorlog


class Logger:
    format = '%(log_color)s%(asctime)s %(levelname)s %(filename)s [line %(lineno)s]: %(message)s'
    datefmt = "%d/%m %H:%M:%S"
    formatter = colorlog.ColoredFormatter(format, datefmt=datefmt)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    @classmethod
    def get_logger(cls, name, loglevel=logging.INFO):
        logger = logging.getLogger(name)
        logger.addHandler(cls.handler)
        logger.setLevel(loglevel)
        logger.propagate = False  # See: https://stackoverflow.com/questions/6729268/log-messages-appearing-twice-with-python-logging
        return logger
