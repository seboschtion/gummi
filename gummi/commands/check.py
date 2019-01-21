import git

import gummi
import gummi.util

class Check():
    def __init__(self):
        self.files = gummi.util.Files()
        self.repo = self.files.get_repo()
        return

    def run(self, quiet):
        self.check(quiet)
        return gummi.exit_code.SUCCESS
    
    def check(self, quiet):
        fetch = self.repo.remotes.origin.fetch()[0]
        diff = self.git_diff()
        if diff:
            if not quiet:
                print("Your document is out of date.")
            return True
        if not quiet:
            print("Your document is up-to-date. Nothing to do.")
        return False

    def git_diff(self):
        return self.repo.head.commit.diff(self.repo.remotes.origin)

