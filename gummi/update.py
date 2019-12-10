from os import makedirs, path, remove, removedirs, listdir
from shutil import copy
from hashlib import sha1
from git import exc
from .check import check, get_diff, get_repo
from . import constants
from . import exit_codes


def add(files):
    for file in files:
        filepath, filename = path.split(file)
        source_filename = path.join(
            constants.MANAGED_FOLDER, constants.TEMPLATE_FOLDER, filepath, filename)
        destination_filename = file
        if check_file_has_changed(source_filename, destination_filename):
            yes = ask_yes_no(
                f"A? {destination_filename} already exists. Do you want to override it? If not, tracking will be lost.")
            if not yes:
                continue
        print(f"A: {destination_filename}")
        if len(filepath) > 0 and not path.exists(filepath):
            makedirs(filepath, exist_ok=True)
        copy(source_filename, destination_filename)
    return True


def update(files):
    for file in files:
        local, original = get_local_and_original(file)
        filepath, filename = path.split(file)
        if len(filepath) > 0 and not path.exists(filepath):
            makedirs(filepath, exist_ok=True)
        copy(original, local)
        print(f"U: {local}")
    return True


def delete(files):
    for file in files:
        try:
            remove(file)
            print(f"D: {file}")
        except OSError:
            pass
        filepath, filename = path.split(file)
        if len(filepath) > 0 and path.isdir(filepath) and len(listdir(filepath)) < 1:
            try:
                removedirs(filepath)
                print(f"  - include empty directory: {filepath}")
            except OSError:
                pass
    return True


def check_file_has_changed(old, new):
    if not path.exists(old) or not path.exists(new):
        return False
    oldsha1 = sha1(
        open(old, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
    newsha1 = sha1(
        open(new, 'r', encoding='ISO-8859-1').read().encode('ISO-8859-1')).digest()
    return not oldsha1 == newsha1


def ask_yes_no(message):
    while True:
        answer = input(f"{message} (yes, no) ").upper()
        if answer.startswith('YES'):
            return True
        elif answer.startswith('NO'):
            return False


def remove_template_folder_from_filepath(filepath):
    if filepath.startswith(constants.TEMPLATE_FOLDER):
        return filepath[len(constants.TEMPLATE_FOLDER) + 1:]
    return filepath


def get_local_and_original(filename):
    old = filename
    new = path.join(constants.MANAGED_FOLDER,
                    constants.TEMPLATE_FOLDER, filename)
    return old, new


def get_changed_files():
    diff = get_diff()
    added, updated, deleted = [], [], []
    for diff_item in diff:
        path = remove_template_folder_from_filepath(diff_item.b_path)
        if diff_item.change_type == 'A':
            added.append(path)
        if diff_item.change_type == 'R':
            rename_from = remove_template_folder_from_filepath(
                diff_item.rename_from)
            rename_to = remove_template_folder_from_filepath(
                diff_item.rename_to)
            added.append(rename_to)
            local, original = get_local_and_original(rename_from)
            if check_file_has_changed(local, original):
                if not ask_yes_no(f"D? {local} has changed locally but the template file has moved. Delete it locally? If not, tracking will be lost."):
                    continue
            deleted.append(rename_from)
        local, original = get_local_and_original(path)
        if diff_item.change_type == 'D':
            if check_file_has_changed(local, original):
                if not ask_yes_no(f"D? {local} has changed locally but was deleted from the template. Delete it locally? If not, tracking will be lost."):
                    continue
            deleted.append(path)
        if diff_item.change_type == 'M':
            if check_file_has_changed(local, original):
                if not ask_yes_no(f"U? {local} has changed locally and the template file has changed, too. Update the local file? If not, tracking will be lost."):
                    continue
            updated.append(path)
    return added, updated, deleted


def pull_repository():
    repo = get_repo()
    try:
        repo.remotes.origin.pull()
        return True
    except exc.GitCommandError:
        print("Could not connect to remote repository.")
    return False


def reset_repository():
    repo = get_repo()
    repo.git.reset('--hard', 'HEAD@{1}')


def run_update_dry(added, updated, deleted):
    print("Find the upcoming changes below:")
    for a in added:
        print(f"A: {a}")
    for u in updated:
        print(f"U: {u}")
    for d in deleted:
        print(f"D: {d}")


def run_update(dry, retry):
    if retry:
        reset_repository()
    if not check():
        return exit_codes.SUCCESS
    added, updated, deleted = get_changed_files()
    if dry:
        run_update_dry(added, updated, deleted)
        return exit_codes.SUCCESS
    if not pull_repository():
        return exit_codes.UNKNOWN
    if not add(added) or not update(updated) or not delete(deleted):
        reset_repository()
        print("Error updating the document. You can retry by adding the --retry argument to the update command.")
        return exit_codes.UNKNOWN
    print("The document was updated successfully.")
    return exit_codes.SUCCESS
