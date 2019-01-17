import os, git

import constants, exit_code
from gummi.config.config import Config

class Init:
    def __init__(self):
        self.config = Config()

    def run(self):
        if self.config.exists():
            print(f"{constants.PROGRAM_NAME} already initialized for this document.")
            return exit_code.ALREADY
        result = self.create_config()
        if result != 0:
            print("Error creating config.")
            return exit_code.UNKNOWN
        print("The document is now initialized, happy typing!")
        return exit_code.SUCCESS

    def create_config(self):
        self.config.init()
        return exit_code.SUCCESS

