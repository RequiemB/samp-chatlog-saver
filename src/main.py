import os
import logging
import sys

from funcs.config import retrieve_configuration
from funcs.saver import SAMPChatLogSaver
from funcs import logger 

# Get the configuration
config = retrieve_configuration('config.json')

saver = SAMPChatLogSaver(config) # Initialize a SAMPChatLogSaver instance with the configuration
if __name__ == '__main__':
    try:
        saver.run() # Run the program
    except KeyboardInterrupt:
        sys.exit()



    

