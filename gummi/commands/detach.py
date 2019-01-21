import os
import shutil
import pathlib

import gummi
import gummi.util

class Detach():
    def __init__(self):
        self.files = gummi.util.Files()

    def run(self):
        self.delete_managed_files()
        self.files.delete_managed_folder()
        print(f"{gummi.constants.PROGRAM_NAME} detached.\nSome files might still be around, delete them manually.")
        return gummi.exit_code.SUCCESS

    def delete_managed_files(self):
        path = self.files.get_template_folder()
        files = list(pathlib.Path(path).rglob('*'))
        if not files: return
        for file in files:
            path, name = os.path.split(file)
            path = self.files.relative_path(path)
            try:
                os.remove(os.path.join(path, name))
                os.removedirs(path)
            except OSError:
                pass

