from conf.logconf import LOGGING_CONFIG
import logging.config
logger=logging.config.dictConfig(LOGGING_CONFIG)
def logrecord(mode):
    logger = logging.getLogger(mode)
    return logger
