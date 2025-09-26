import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

file_handler = RotatingFileHandler(
    "app.log", maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setFormatter(formatter)


logger = logging.getLogger("app/logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
