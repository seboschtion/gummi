from shutil import rmtree
from . import constants


def delete_managed():
    rmtree(constants.MANAGED_FOLDER)


def run_detach():
    delete_managed()
    print("Detached. Bye.")
