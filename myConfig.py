# autor : luka fricker
# date  : 19.01.2024

# description : simple class to get and store settings as a python file for values that should persist application restart

import pathlib
import json
import os


class myConfig:
    def __init__(self):
        parent_path = pathlib.Path(__file__).parent.resolve()
        self.__path = os.path.join(parent_path, "config.json")

    def get_config(self):
        try:
            with open(self.__path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
            return config_data
        except FileNotFoundError:
            print(f"Error: File '{self.__path}' not found.")
            return {}

    def set_config(self, config):
        try:
            with open(self.__path, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=4)
            print(f"Configurations successfully saved to '{self.__path}'.")
        except Exception as e:
            print(f"Error: Unable to save configurations to '{self.__path}'. {e}")
