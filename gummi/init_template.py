import os

import constants
from gummi.config import Config

class InitTemplate:
    def __init__(self):
        self.config = Config()
        return

    def run(self):
        if self.config.exists():
            print(f"Having a template document managed by {constants.BINARY_NAME} is not recommended.")
            return
        try:
            os.mkdir(constants.TEMPLATE_FOLDER)
        except OSError:
            print("There was an error. Does the `{constants.TEMPLATE_FOLDER}` folder already exist?")
            return
        print("Done. Add your shared files into the `{constants.TEMPLATE_FOLDER}` folder")

