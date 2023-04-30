import json
import os

from tkinter import Tk, filedialog, PhotoImage
from .saver import wait_until_response
from . import logger

# Create Tkinter instance for folder prompt
window = Tk()
window.withdraw()

window.attributes('-topmost')

# Set the GUI icon

icon = PhotoImage(file="./icon.png")
window.iconphoto(False, icon)

# Get the SAMP path
def request_path(dir_type):

    doc_path = f"{os.getenv('HOMEDRIVE')}/{os.getenv('HOMEPATH')}/Documents/"

    path: str
    try:
        path = filedialog.askdirectory(initialdir=doc_path, title=f"Select your {dir_type} folder")
    except:
        path = filedialog.askdirectory(title=f"Select your {dir_type} folder")

    if dir_type == "SAMP":
        if path == "":
            logger.warning(f"The prompt dialog was closed by the user. Chatlog saver cannot run with an invaild {dir_type} path.")
            wait_until_response(wait_type=1)

    return path

# Generate a JSON configuration file

def generate_json(path: str):
    try:
        os.remove(path)
    except:
        pass

    json_file = open(path, "w+")

    # The default path to be used in case the user doesn't select the dirs
    default_path = f"{os.getenv('HOMEDRIVE')}/{os.getenv('HOMEPATH')}/Documents/GTA San Andreas User Files/SAMP/"

    data = {}

    data["windowed_instance"] = True

    samp_path = request_path("SAMP")
    log_path = request_path("SAMP Log")

    data["samp_path"] = samp_path
    data["log_path"] = log_path

    if samp_path == "":
        data["samp_path"] = default_path

    if log_path == "":
        data["log_path"] = os.path.join(default_path, "logs")

    json.dump(data, json_file, indent=4)

    return data

def retrieve_configuration(file: str): # Retrieves the configuration from the file, i.e. the paths, the prefrences 
    data = {}
    try:
        data = json.load(open(file, "r"))
    except FileNotFoundError: # Create the file again if it wasn't found
        logger.warning(f" No configuration file was found. Generating a JSON file...")
        data = generate_json(file)
    except json.decoder.JSONDecodeError: # The file isn't in the JSON format. Make another one
        logger.warning(f" {file} is not in the JSON format. Regenerating another one...")
        data = generate_json(file)
    except Exception as e: # An Exception has occured. Catch it and log it
        print(f"An error occured while opening the file. Error Info: {e.errno}")
        wait_until_response(wait_type=1)
    
    assert data is not {} # Make sure that data is not an empty variable

    config = {} # Create a dict to store the formatted data
 
    try: # Try to access the data inside
        if data["samp_path"] is None: # If samp_path is not set, prompt the user to select the path again
            path = request_path("SAMP")
            config["samp_path"] = path
            logger.warning(f"No SAMP path was found in the configuration, select your desired path.")
        else:
            if not os.path.exists(data["samp_path"]): # If the path given is invalid, prompt the user to select the path again
                logger.error(f"The SAMP User files path ({data['samp_path']}) is not valid. select the path again.")
                config["samp_path"] = request_path("SAMP")
            else:  # If the path is valid, store it into the config
                config["samp_path"] = data["samp_path"]

    except KeyError: # If samp_path is not a key in the configuration, raise an error
        logger.error("The path 'samp_path' was not found in the configuration. Generating another one...")
        generate_json(file)
        wait_until_response(wait_type=1)

    try: # Check if it's a valid SAMP directory
        if not os.path.exists(config["samp_path"]+'\\sa-mp.cfg'):
            logger.error(f" The path used is not a valid SA-MP User Files path. Select the path again.\n Path: {config['samp_path']}.")
            path = request_path("SAMP")
            config["samp_path"] = path
    except Exception:
        logger.warning("An exception has occured. Restart the program.")
        wait_until_response(wait_type=1)

    try:
        if data["log_path"] is None: # If log_path is not set, prompt the user to select a directory
            logger.warning(f"No log path was set. Select the path.")
            path = request_path("SAMP Log")
            config["log_path"] = path
            if path == "": # If the user didn't give a path, use the default one
                config["log_path"] = os.path.join(config["samp_path"], "logs")
                try: # Create the default logs folder
                    os.mkdir(config["log_path"])
                except FileExistsError: # Ignore if the folder already exists
                    pass
        else:
            if not os.path.exists(data["log_path"]): # If the path given is invalid, create that folder
                try:
                    os.mkdir(data["log_path"])
                    config["log_path"] = data["log_path"]
                except:
                    logger.error(f" An error occured while attempting to create the logging folder: {data['log_path']}. Choose the path yourself.")
                    path = request_path("SAMP Log")
                    config["log_path"] = path
            else: # If the path exists, store it into the config
                config["log_path"] = data["log_path"]


    except KeyError: # If log_path is not a key in the configuration, raise an error
        logger.error("The path 'log_path' was not found in the configuration. Regenerating another configuration... Run the program again.")
        generate_json(file)
        wait_until_response(wait_type=1)

    try:
        if data["windowed_instance"] is False: # Whether the program should run with a console window
            config["windowed_instance"] = False
        else:
            config["windowed_instance"] = True

    except KeyError: # The var 'windowed_instance' is not a key in the configuration
        config["windowed_instance"] = True # It's true by default
        data["windowed_instance"] = True
        json.dump(data, open(file, "w"), indent=4) # Dump the new added var into the file

    assert config is not {} # Make sure config is not an empty dict

    json.dump(config, open(file, "w"), indent=4)

    # We've added all the config into the dict, now we can return the dict
    return config