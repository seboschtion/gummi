import shutil, os
from pathlib import Path

import constants
from gummi.util import remove_dotpath
from gummi.config import Config
from gummi.check import Check
from gummi.ldmgit import LdmGit

class Update:
    def __init__(self):
        self.check = Check()
        self.config = Config()
        self.git = LdmGit()
        return

    def run(self):
        updates_available = self.check.run(quiet=True)
        if not updates_available:
            print("Your document is up-to-date with original. Redoing some things anyway.")
        deleted = self.find_deleted_files()
        self.git.pull()
        self.delete_files(deleted)
        self.add_files()
        print("The document is now updated.")

    def delete_files(self, files):
        for file in files:
            path, name = os.path.split(file)
            os.remove(file)
            if not path == '':
                os.removedirs(path)

    def find_deleted_files(self):
        diff = self.git.diff()
        base_path = os.path.join(constants.LDM_FOLDER, self.config.get_source_name())
        deleted = []
        for diff_item in diff:
            if diff_item.change_type == 'D':
                path = diff_item.b_path
                first_slash = path.find('/') + 1
                deleted.append(path[first_slash:])
        return deleted

    def add_files(self):
        path = os.path.join(constants.LDM_FOLDER, self.config.get_source_name(), constants.LDM_TEMPLATE_FOLDER)
        new_files = list(Path(path).rglob('*'))
        if not new_files:
            print("Warning: There is either no `ldm` folder in the template or no files ar inisde it.")
            return False
        for file in new_files:
            if os.path.isdir(file):
                continue
            path, name = os.path.split(file)
            destination = remove_dotpath(path)
            try:
                os.makedirs(destination)
            except OSError:
                pass
            shutil.copy(file, destination)
        return True

