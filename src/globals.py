import logging

from environs import Env

env = Env()
LOG_LEVEL = env.log_level("LOG_LEVEL", logging.WARNING)
VERBOSE = LOG_LEVEL <= logging.INFO
