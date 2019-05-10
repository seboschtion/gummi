from git import Repo, exc
from rfc3987 import match
from shutil import rmtree
from os import mkdir, path, walk
from .update import add
from .detach import delete_managed
from . import constants
from . import exit_codes


def ask_source():
    while True:
        source = input("Enter the template git repository: ")
        if match(source, rule='IRI'):
            return source
        print(f"Please try another git repository than {source}.")
    return ""


def clone_git_repo(source):
    try:
        cloned_repo = Repo.clone_from(
            source, constants.MANAGED_FOLDER, branch='master')
    except exc.GitError as e:
        print(e)
        return False
    return path.isdir(cloned_repo.working_tree_dir)


def list_all_files():
    all_files = []
    template_folder = path.join(
        constants.MANAGED_FOLDER, constants.TEMPLATE_FOLDER)
    for (abs_directory, _, abs_filenames) in walk(template_folder):
        if abs_directory.startswith(template_folder):
            rel_directory = abs_directory[len(template_folder) + 1:]
        for abs_filename in abs_filenames:
            all_files.append(path.join(rel_directory, abs_filename))
    return all_files


def run_init():
    source = ask_source()
    mkdir(constants.MANAGED_FOLDER)
    if not clone_git_repo(source):
        print(f"Could not clone {source}.")
        delete_managed()
        return exit_codes.INVALID_SOURCE
    print("The document is now initialized, happy typing!")
    if add(list_all_files()):
        return exit_codes.SUCCESS
    else:
        delete_managed()
        return exit_codes.UNKNOWN


def run_init_template():
    if path.exists(constants.TEMPLATE_FOLDER):
        print(
            f"There was an error. The `{constants.TEMPLATE_FOLDER}` folder already exists.")
        return exit_codes.ALREADY
    mkdir(constants.TEMPLATE_FOLDER)
    gitignore = open('.gitignore', 'w')
    gitignore.write(constants.MANAGED_FOLDER)
    gitignore.write("\n")
    gitignore.close()
    print(
        f"Done. Add your shared files into the `{constants.TEMPLATE_FOLDER}` folder.")
    return exit_codes.SUCCESS
