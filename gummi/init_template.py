import os

import constants
from gummi.config import Config

class InitTemplate:
    def __init__(self):
        self.config = Config()
        return

    def run(self):
        if self.config.exists():
            print("Having a template document managed by ldm is not recommended.")
            return
        try:
            os.mkdir(constants.LDM_TEMPLATE_FOLDER)
        except OSError:
            print("There was an error. Does the `ldm` folder already exist?")
            return
        print("Done. Add your shared files into the `ldm` folder")

