import os, git

import constants
from gummi.config import Config
from gummi.update import Update

class Init:
    def __init__(self):
        self.config = Config()
        return

    def run(self, source=None):
        if self.config.exists():
            print("This document already is managed by ldm.")
            return
        if not self.create_config(source):
            print("Error creating config.")
            return
        if not self.clone_repo():
            print("Error cloning templates.")
            return
        update = Update()
        update.add_files()
        print("The document is now initialized, happy typing!")

    def create_config(self, source=None):
        while True:
            if not source:
                source = input("Enter the template git repository: ")
            name = self.get_name_of_gitrepo(source)
            if not name == None:
                self.config.set_source_url(source)
                self.config.set_source_name(name)
                break
            else:
                source = ''
                print("This seems not to be a valid Git repository URL.")
        return True

    def get_name_of_gitrepo(self, url):
        last_slash_index = url.rfind('/')
        last_dot_index = url.rfind('.')
        if last_slash_index == -1 or last_dot_index == -1:
            return None
        return url[last_slash_index + 1:last_dot_index]

    def clone_repo(self):
        ldm_folder = os.path.join(os.getcwd(), constants.LDM_FOLDER)
        os.mkdir(ldm_folder)
        try:
            git.Git(ldm_folder).clone(self.config.get_source_url())
        except git.exc.GitError as e:
            print(e)
            return False
        return True

