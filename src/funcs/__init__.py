# For relative imports to work in Python 3.6
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import logging

# Set up logging

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.propagate = False

# Add a handler to the logger
logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setLevel(logging.INFO)

logger_formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(message)s")
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)

# Make a file handler if the user has 'file_log' enabled
file_handler = logging.FileHandler(os.path.join(sys.path[0], "saver.log"))
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)
