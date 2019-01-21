import git
import rfc3987

import gummi
import gummi.util

class Init():
    def __init__(self):
        self.files = gummi.util.Files()

    def run(self):
        source = self.__ask_source()
        self.files.init_document()
        if not self.__clone_repo(source):
            print(f"Could not clone {source}.")
            self.files.delete_managed_folder()
            return gummi.exit_code.INVALID_SOURCE
        gummi.commands.Update().add_files()
        print("The document is now initialized, happy typing!")
        return gummi.exit_code.SUCCESS

    def __ask_source(self):
        while True:
            source = input("Enter the template git repository: ")
            if rfc3987.match(source, rule='IRI'):
                break
            print(f"Please try another git repository than {source}.")
        return source

    def __clone_repo(self, source):
        try:
            git.Git(gummi.constants.MANAGED_FOLDER).clone(source)
        except git.exc.GitError as e:
            print(e)
            return False
        return True

