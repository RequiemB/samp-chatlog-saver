import os
import sys
import logging
import time

from funcs.config import retrieve_configuration
from funcs.saver import SAMPChatLogSaver, is_process_running
from funcs import logger 

# Add a file handler
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), "saver.log"))
file_handler.setLevel(logging.INFO)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# Check if the chatlog is already running
def check_if_already_running() -> None:
    if is_process_running('chatlog-saver.exe'):
        value = input("Another instance of this chat-log saver is being run. Do you want to close it and initate this instance? (Y/N): ")
        if value.lower() not in ['y', 'n']:
            print("Invalid input.")
            check_if_already_running()
        if value.lower() == "y":
            os.system("TASKKILL /im chatlog-saver.exe /f")
            pass
        else:
            print("Quitting this instance...")
            time.sleep(1)
            sys.exit()

# Get the configuration
config = retrieve_configuration(os.path.join(os.path.dirname(__file__), "config.json"))

saver = SAMPChatLogSaver(config) # Initialize a SAMPChatLogSaver instance with the configuration
if __name__ == '__main__':
    try:
        saver.run() # Run the program
    except KeyboardInterrupt:
        sys.exit()



    

