import os, shutil

import gummi
import gummi.util

class Detach():
    def __init__(self):
        self.files = gummi.util.Files()

    def run(self):
        self.files.delete_managed_folders()
        self.files.delete_config() 
        print(f"{gummi.constants.PROGRAM_NAME} detached.\nSome files might still be around, delete them manually.")
        return gummi.exit_code.SUCCESS

