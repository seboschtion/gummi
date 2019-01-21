import os
import shutil
import git

import gummi

class Files:
    def init_document(self):
        try:
            os.mkdir(gummi.constants.MANAGED_FOLDER)
        except OSError:
            pass

    def init_template(self):
        try:
            os.mkdir(gummi.constants.TEMPLATE_FOLDER)
            return True
        except OSError:
            pass
        return False

    def is_initialized(self):
        managed_folder_exists = os.path.isdir(gummi.constants.MANAGED_FOLDER)
        if not managed_folder_exists: return False
        repo_cloned = len(os.listdir(gummi.constants.MANAGED_FOLDER)) > 0
        return repo_cloned

    def delete_managed_folder(self):
        try:
            shutil.rmtree(gummi.constants.MANAGED_FOLDER)
        except IOError:
            pass

    def get_repo(self):
        return git.Repo(self.get_repo_folder())

    def get_template_folder(self):
        repo = self.get_repo_folder()
        return os.path.join(repo, gummi.constants.TEMPLATE_FOLDER)

    def relative_path(self, path):
        dotpath = self.get_template_folder()
        path = path.replace(dotpath, '')
        if path.find('/') == 0:
            path = path[1:]
        if path == '':
            path = '.'
        return path

    def get_repo_folder(self):
        all_files = os.listdir(gummi.constants.MANAGED_FOLDER)
        return os.path.join(gummi.constants.MANAGED_FOLDER, all_files[0])

