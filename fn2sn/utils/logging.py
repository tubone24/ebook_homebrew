import os
import logging
from logging import config
import yaml

yaml_path = os.path.join(os.path.dirname(__file__), "logging.yaml")

with open(yaml_path) as f:
    dict_config = yaml.load(f)

config.dictConfig(dict_config)


class AppLog:

    logger = None

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def debug(self, msg, *args):
        self.logger.debug(msg, *args)

    def info(self, msg, *args):
        self.logger.info(msg, *args)

    def warn(self, msg, *args):
        self.logger.warning(msg, *args)

    def error(self, msg, *args):
        self.logger.error(msg, *args)

    def exception(self, msg, *args):
        self.logger.exception(msg, *args)

    def critical(self, msg, *args):
        self.logger.critical(msg, *args)


def get_logger(name):
    return AppLog(name)

