from git import Repo, exc
from . import constants
from . import exit_codes


def get_repo():
    return Repo(constants.MANAGED_FOLDER)


def get_diff():
    repo = get_repo()
    return repo.head.commit.diff(repo.remotes.origin)


def fetch():
    repo = get_repo()
    repo.remotes.origin.fetch()[0]


def check():
    try:
        fetch()
    except exc.GitCommandError:
        print("Could not connect to remote repository.")
        return False
    if get_diff():
        print("Your document is out of date.")
        return True
    print("Your document is up-to-date. Nothing to do.")
    return False


def run_check():
    check()
    return exit_codes.SUCCESS
