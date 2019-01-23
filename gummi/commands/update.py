import os
import shutil
import pathlib
import hashlib

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
        updated = self.__find_updated_files()
        self.repo.remotes.origin.pull()
        self.__delete_files(deleted)
        self.__update_files(updated)
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
            newfile = os.path.join(destination, name)
            if not self.__check_file_has_changed(file, newfile):
                shutil.copy(file, destination)
        return True

    def __check_file_has_changed(self, old, new):
        if not os.path.exists(old) or not os.path.exists(new):
            return False 
        oldsha1 = hashlib.sha1(open(old, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
        newsha1 = hashlib.sha1(open(new, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
        return not oldsha1 == newsha1

    def __delete_files(self, files):
        for file in files:
            path, name = os.path.split(file)
            os.remove(file)
            if not path == '':
                try:
                    os.removedirs(path)
                except OSError:
                    pass

    def __update_files(self, files):
        for file in files:
            old, new = self.__get_old_and_new(file)
            shutil.copy(new, old)

    def __find_updated_files(self):
        diff = self.check.git_diff()
        updated = []
        for diff_item in diff:
            if diff_item.change_type == 'M':
                path = diff_item.b_path
                first_slash = path.find('/') + 1
                updated_path = path[first_slash:]
                old, new = self.__get_old_and_new(updated_path)
                if self.__check_file_has_changed(old, new):
                    print(f"{old} has changed locally and remotely. It will not be updated here.")
                else:
                    updated.append(updated_path)
        return updated

    def __find_deleted_files(self):
        diff = self.check.git_diff()
        deleted = []
        for diff_item in diff:
            if diff_item.change_type == 'D':
                path = diff_item.b_path
                first_slash = path.find('/') + 1
                delete_path = path[first_slash:]
                old, new = self.__get_old_and_new(delete_path)
                if self.__check_file_has_changed(old, new):
                    print(f"{old} has changed locally and deleted remotely. From now on, it is your responsibility to keep track of that file!")
                else:
                    deleted.append(delete_path)
        return deleted

    def __get_old_and_new(self, filename):
        old = filename
        new = os.path.join(self.files.get_template_folder(), filename)
        return old, new
        
