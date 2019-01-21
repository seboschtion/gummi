import os
import shutil
import pathlib

import gummi
import gummi.util
import gummi.commands

class Update():
    def __init__(self):
        self.files = gummi.util.Files()
        self.check = gummi.commands.Check()
        self.repo = self.files.get_repo()

    def run(self):
        updates_available = self.check.check(quiet=True)
        if not updates_available:
            print("Your document is up-to-date. Redoing some things anyway.")
        deleted = self.__find_deleted_files()
        self.repo.remotes.origin.pull()
        self.__delete_files(deleted)
        self.add_files()
        print("The document is now updated.")
        return gummi.exit_code.SUCCESS

    def add_files(self):
        path = self.files.get_template_folder()
        new_files = list(pathlib.Path(path).rglob('*'))
        if not new_files:
            print(f"Warning: There is either no `{gummi.constants.TEMPLATE_FOLDER}` folder in the template or no files ar inisde it.")
            return False
        for file in new_files:
            if os.path.isdir(file):
                continue
            path, name = os.path.split(file)
            destination = self.files.relative_path(path)
            try:
                os.makedirs(destination)
            except OSError:
                pass
            shutil.copy(file, destination)
        return True

    def __delete_files(self, files):
        for file in files:
            path, name = os.path.split(file)
            os.remove(file)
            if not path == '':
                try:
                    os.removedirs(path)
                except OSError:
                    pass

    def __find_deleted_files(self):
        diff = self.check.git_diff()
        base_path = self.files.get_repo_folder()
        deleted = []
        for diff_item in diff:
            if diff_item.change_type == 'D':
                path = diff_item.b_path
                first_slash = path.find('/') + 1
                deleted.append(path[first_slash:])
        return deleted
