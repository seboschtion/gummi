import os
from git import Repo

import constants
from gummi.config import Config
from gummi.ldmgit import LdmGit

class Check:
    def __init__(self):
        self.config = Config()
        self.git = LdmGit()
        return

    def run(self, quiet=False):
        self.git.fetch()
        if self.git.diff():
            if not quiet:
                print("Your document is out of date. Run `ldm update`.")
            return True
        if not quiet:
            print("Your document is up-to-date. Nothing to do.")
        return False

