# SA-MP Chatlog Saver

A chatlog saver for the multiplayer modification of GTA San Andreas, San Andreas Multiplayer (SA-MP).

![image](https://img.shields.io/badge/Python-3.8-blue.svg)

## Usage
  
In order to use the program, head over to the [Releases](https://github.com/RequiemB/samp-chatlog-saver/releases/tag/v.1.0.0) page and install the executable from the latest release. It's recommended to make a new folder and put it inside there. After downloading, run the program once to generate the configuration. A box will pop up asking for your SAMP path and your preferred log path, set it as you like. That's it, you can now join a server and when you quit, the chatlog will be saved.

## Configuration 

The configuration will be in this format:
```json
{
  "samp_path": "<your-samp-path>",
  "log_path": "<your-log-path>",
  "windowed_instance": true
}
```

The configs 'samp_path' and 'log_path' are set manually when you run the program. You'll have to edit the 'windowed_instance' value if you do not want a console window open. 
If you want a console window when you run the program, edit the file as follows: 
```json
{
  "samp_path": "<your-samp-path>",
  "log_path": "<your-log-path>",
  "windowed_instance": true
}
```

If you do not want a console window when you run the program, edit the file as follows:
```json
{
  "samp_path": "<your-samp-path>",
  "log_path": "<your-log-path>",
  "windowed_instance": false
}
```
**Note: It's recommended to add any more configurations or edit the variables other than 'windowed_instance' yourself, if you did and the program isn't running correctly, just delete the file and the program will generate another one.**

## Running via Python

In order to run the program via Python, run the following commands in your console:

```sh
git clone https://github.com/RequiemB/samp-chatlog-saver.git
cd ./samp-chatlog-saver
python main.py
```

**Note: Make sure you have Python 3.6+ installed.**

## License

This repository is licensed under the MIT License.

## Contact

If you're facing any issues, contact me at Requiem#8722.
