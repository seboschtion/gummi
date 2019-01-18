import os, shutil

import gummi.constants as constants
import gummi.exit_code as exit_code
from gummi.config import Config

class Detach:
    def __init__(self):
        self.config = Config()

    def run(self):
        try:
            shutil.rmtree(constants.MANAGED_FOLDER)
        except IOError:
            pass
        try:
            os.remove(constants.CONFIG_FILENAME)
        except OSError:
            pass
        print(f"{constants.PROGRAM_NAME} detached.\nSome files might still be around, delete them manually.")
        return exit_code.SUCCESS

