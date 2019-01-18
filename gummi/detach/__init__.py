import os, shutil

import gummi.constants as constants
import gummi.exit_code as exit_code
from gummi.config import Config
from gummi.filesystem import Filesystem    

class Detach:
    def __init__(self):
        self.config = Config()
        self.filesystem = Filesystem()

    def run(self):
        self.filesystem.delete_managed_folders()
        self.filesystem.delete_config() 
        print(f"{constants.PROGRAM_NAME} detached.\nSome files might still be around, delete them manually.")
        return exit_code.SUCCESS

