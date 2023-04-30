import subprocess
import datetime
import win32gui
import win32.lib.win32con as win32con
import sys
import time
import re
import os

from . import logger

IP = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):\d{1,5}"

def wait_until_response(wait_type: int = 0, msg: str = None): 
    try:
        if wait_type == 0 and msg is not None: # Waiting for a key press to continue
            input(msg)
        if wait_type == 1: # Waiting for a key press to exit the program
            input("Press Enter to exit the program...")
    except SyntaxError: # The code is being run on Python 2.x
        sys.exit()
    if wait_type == 1:
        sys.exit()
    else:
        pass
        
def construct_datetime(): # Function to format the datetime in our chatlog format
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, "%d_%m_%Y_%H_%M_%S")
    return now_str

def is_process_running(process: str): # Used to check if a process is running, in this case gta_sa.exe
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process.lower())

def close_console_window(): # Closes the console window if 'windowed_instance' in configuration is set to False.
    console = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console, win32con.SW_HIDE)

class SAMPChatLogSaver:
    def __init__(self, data: dict):
        # Load all the data and store them into variables
        self.samp_path = data.get("samp_path")
        self.log_path = data.get("log_path")
        self.windowed = data.get("windowed_instance")

    def run(self): # To run the program
        # Print the config into the console
        logger.warning(f"SAMP Chatlog Saver is running with the following configuration:\n   SAMP Path: {self.samp_path}\n   Log Path: {self.log_path}\n   Windowed Instance: {self.windowed}.")

        # Delay the closing for the user to double-check
        time.sleep(2)

        # Close the console window if 'windowed_instance' is False
        if not self.windowed:
            close_console_window()

        while True: # A forever loop to check if gta_sa is running
            if is_process_running('gta_sa.exe'):
                break # Break the loop if it's running
            else:
                time.sleep(5)

        print("GTA San Andreas has initalized. Waiting for the program termination.", flush=True)

        while True: # A forever loop to check if gta_sa is closed
            if not is_process_running('gta_sa.exe'):
                break # Break the loop if it's closed
            else:
                time.sleep(2)

        self.save_log() # Save the log

        if not self.windowed:
            sys.exit() # Exit the program if it's not windowed
        else:
            self.run() # Run the program again if it's windowed


    def save_log(self):
        log = open(os.path.join(self.samp_path, "chatlog.txt"), 'r')
        content = log.read()

        # Format the filename

        fname = "SAMP_Log_{}.txt".format(construct_datetime())

        # Extracting the IP address from the content

        # Compile the regex
        ip_regex = re.compile(IP)

        # We split the content till line 4 and loop through every line to check for the IP
        # This is because of mods loading messages appearing before the IP can interfere with the checking
        for line in content.split('\n')[:4]:
            if re.search(ip_regex, line): # Search for the IP address in the line using the IP
                ip_str = re.findall(ip_regex, line)[0].split(":") # Extract it and split it 

        assert ip_str is not None

        # ip_str is now a list like ['127.0.0.1', '7777']
        # We join it with '_' so we get a result like '127.0.0.1_7777'
        ip = "_".join(ip_str)

        if not os.path.exists(os.path.join(self.log_path, ip)): # If the IP doesn't exist as a folder, create one
            os.mkdir(os.path.join(self.log_path, ip))

        # Create the new log file and write the content in there and close the file

        path = os.path.join(self.log_path, ip, fname)

        log_file = open(path, 'w')
        log_file.write(content)
        log_file.close()

        logger.warning(f"Log has been saved to {path}.")

        return True