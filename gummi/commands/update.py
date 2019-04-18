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

    def run(self, dry):
        updates_available = self.check.check(quiet=True)
        if not updates_available:
            print("Your document is already up-to-date.")
            return gummi.exit_code.SUCCESS
        added, updated, deleted = self.__find_changed_files()
        if dry:
            print("Will add:")
            print(added)
            print("Will update:")
            print(updated)
            print("Will delete:")
            print(deleted)
            return gummi.exit_code.SUCCESS
        self.repo.remotes.origin.pull()
        self.__delete_files(deleted)
        self.__update_files(updated)
        self.add_files(added)
        print("The document is now updated.")
        return gummi.exit_code.SUCCESS

    def add_files(self, files):
        for file in files:
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
        oldsha1 = hashlib.sha1(
            open(old, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
        newsha1 = hashlib.sha1(
            open(new, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
        return not oldsha1 == newsha1

    def __delete_files(self, files):
        for file in files:
            path, name = os.path.split(file)
            try:
                os.remove(file)
            except OSError:
                pass
            if not path == '':
                try:
                    os.removedirs(path)
                except OSError:
                    pass

    def __update_files(self, files):
        for file in files:
            old, new = self.__get_old_and_new(file)
            shutil.copy(new, old)

    def __find_changed_files(self):
        diff = self.check.git_diff()
        added, updated, deleted = [], [], []
        for diff_item in diff:
            path = diff_item.b_path
            first_slash = path.find('/') + 1
            path = path[first_slash:]
            old, new = self.__get_old_and_new(path)
            if self.__check_file_has_changed(old, new):
                print(f"{old} changed locally, so no modifications done.")
            else:
                if diff_item.change_type == 'A':
                    added.append(self.files.absolute_path(path))
                if diff_item.change_type == 'M':
                    updated.append(path)
                if diff_item.change_type == 'D':
                    deleted.append(path)
        return added, updated, deleted

    def __get_old_and_new(self, filename):
        old = filename
        new = os.path.join(self.files.get_template_folder(), filename)
        return old, new
