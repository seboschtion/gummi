import os, shutil
from pathlib import Path

import constants
from gummi.util import remove_dotpath
from gummi.config import Config

class Reset:
    def __init__(self):
        self.config = Config()
        return

    def run(self):
        self.delete_managed_files()
        try:
            shutil.rmtree(constants.MANAGED_FOLDER)
        except IOError:
            pass
        try:
            os.remove(constants.CONFIG_FILENAME)
        except OSError:
            pass
        print("Document resetted. Some files and other garbage might still be around, delete it manually.")

    def delete_managed_files(self):
        config = self.config.get_source_name()
        if not config:
            return
        path = os.path.join(constants.MANAGED_FOLDER, config, constants.TEMPLATE_FOLDER)
        files = list(Path(path).rglob('*'))
        if not files:
            return
        for file in files:
            path, name = os.path.split(file)
            path = remove_dotpath(path)
            try:
                os.remove(os.path.join(path, name))
                os.removedirs(path)
            except OSError:
                pass

