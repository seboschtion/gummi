import os, shutil

import gummi.constants as constants

class Filesystem:
    def init(self):
        for folder in self.managed_folders():
            os.mkdir(folder)

    def is_initialized(self):
        for folder in self.managed_folders():
            if not os.path.isdir(folder):
                return False
        return True

    def managed_folders(self):
        root = constants.MANAGED_FOLDER
        packages = os.path.join(root, constants.MANAGED_FOLDER_PACKAGES)
        return [root, packages]

    def delete_managed_folders(self):
        try:
            shutil.rmtree(constants.MANAGED_FOLDER)
        except IOError:
            pass

    def delete_config(self):
        try:
            os.remove(constants.CONFIG_FILENAME)
        except OSError:
            pass

