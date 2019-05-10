from shutil import rmtree
import constants


def delete_managed():
    rmtree(constants.MANAGED_FOLDER)


def run_detach():
    delete_managed()
    print("Detached. Bye.")
