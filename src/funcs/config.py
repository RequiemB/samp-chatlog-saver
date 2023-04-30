import json
import os

from .saver import wait_until_response
from . import logger

def generate_json(path: str):
    try:
        os.remove(path)
    except:
        pass

    data = {}

    data["samp_path"] = None
    data["log_path"] = None
    data["windowed_instance"] = True

    file = open("config.json", "w") 
    json.dump(data, file, indent=4)

    return data

def retrieve_configuration(file: str): # Retrieves the configuration from the file, i.e. the paths, the prefrences 
    data = {}
    try:
        data = json.load(open(file, "r"))
        print("jhelo", flush=True)
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

    default_path = f"{os.getenv('HOMEDRIVE')}/{os.getenv('HOMEPATH')}/Documents/GTA San Andreas User Files/SAMP/"
 
    try: # Try to access the data inside
        if data["samp_path"] is None: # If samp_path is not set, use the default SAMP path
            config["samp_path"] = default_path
            logger.info(f"No SAMP path was found in the configuration, using the default SAMP path: ({default_path})")
        else:
            if not os.path.exists(data["samp_path"]): # If the path given is invalid, raise an error
                logger.error(f"The SAMP User files path ({data['samp_path']}) is not valid. Try checking the path again.")
                wait_until_response(wait_type=1)
            else:  # If the path is valid, store it into the config
                config["samp_path"] = data["samp_path"]

    except KeyError: # If samp_path is not a key in the configuration, raise an error
        logger.error("The path 'samp_path' was not found in the configuration. Check my GitHub page for instructions on how to configure the program. (https://www.github.com/RequiemB/SAMP-Chatlog-Saver)")
        wait_until_response(wait_type=1)

    try: # Check if it's a valid SAMP directory
        if not os.path.exists(config["samp_path"]+'\\sa-mp.cfg'):
            logger.error(f" The path used is not a valid SA-MP User Files path. Double-check the path again.\n Path: {config['samp_path']}.")
            wait_until_response(wait_type=1)
    except Exception:
        logger.warning(" An exception has occured. Restart the program.")
        wait_until_response(wait_type=1)

    try:
        if data["log_path"] is None: # If log_path is not set, use the default log path
            config["log_path"] = default_path + 'logs/'
            try: # Create the default logs folder
                os.mkdir(config["log_path"])
            except FileExistsError: # Ignore if the folder already exists
                pass
            logger.info(f"No log path was found in the configuration, using the default log path: ({config['log_path']})")
        else:
            if not os.path.exists(data["log_path"]): # If the path given is invalid, create that folder
                try:
                    os.mkdir(data["log_path"])
                    config["log_path"] = data["log_path"]
                except:
                    logger.error(f" An error occured while attempting to create the folder: {data['log_path']}. Try creating it yourself.")
                    wait_until_response(wait_type=1)
            else: # If the path exists, store it into the config
                config["log_path"] = data["log_path"]


    except KeyError: # If log_path is not a key in the configuration, raise an error
        logger.error("The path 'log_path' was not found in the configuration. Check my GitHub page for instructions on how to configure the program. (https://www.github.com/RequiemB/SAMP-Chatlog-Saver)")
        wait_until_response(wait_type=1)

    try:
        if data["windowed_instance"] is False: # Whether the program should run with a console window
            config["windowed_instance"] = False
        else:
            config["windowed_instance"] = True

    except KeyError: # The var 'windowed_instance' is not a key in the configuration
        config["windowed_instance"] = True # It's true by default
        data["windowed_instance"] = True
        json.dump(open(file, "w"), data, indent=4) # Dump the new added var into the file

    assert config is not {} # Make sure config is not an empty dict

    # We've added all the config into the dict, now we can return the dict
    return config