import os
from git import Repo

import constants
from gummi.config import Config

class Git:
    def __init__(self):
        self.config = Config()
        repo_path = os.path.join(constants.MANAGED_FOLDER, self.config.get_source_name())
        self.repo = Repo(repo_path)
        return

    def diff(self):
        return self.repo.head.commit.diff(self.repo.remotes.origin)

    def fetch(self):
        return self.repo.remotes.origin.fetch()[0]

    def pull(self):
        return self.repo.remotes.origin.pull()[0]

