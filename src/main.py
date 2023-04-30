import os
import sys
import logging

from funcs.config import retrieve_configuration
from funcs.saver import SAMPChatLogSaver
from funcs import logger 

from win32event import CreateMutex
from win32api import GetLastError
from winerror import ERROR_ALREADY_EXISTS

# Add a file handler
file_handler = logging.FileHandler("./saver.log")
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# Thanks to https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s09.html
handle = CreateMutex(None, 1, 'chatlog-saver.exe')

# Check if the chatlog is already running
if GetLastError() == ERROR_ALREADY_EXISTS:
    logger.warning("Another instance of this program is already being run. Running it twice may save the chatlogs twice.")

# Get the configuration
config = retrieve_configuration("./config.json")
saver = SAMPChatLogSaver(config) # Initialize a SAMPChatLogSaver instance with the configuration
try:
    saver.run() # Run the program
except KeyboardInterrupt:
    sys.exit()



    

