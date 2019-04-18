import git
import rfc3987

import gummi
import gummi.util


class Init():
    def __init__(self):
        self.files = gummi.util.Files()

    def init_doc(self):
        source = self.__ask_source()
        self.files.init_document()
        if not self.__clone_repo(source):
            print(f"Could not clone {source}.")
            self.files.delete_managed_folder()
            return gummi.exit_code.INVALID_SOURCE
        files = self.files.list_all_files(self.files.get_template_folder())
        gummi.commands.Update().add_files(files)
        print("The document is now initialized, happy typing!")
        return gummi.exit_code.SUCCESS

    def init_template(self):
        if self.files.init_template():
            print(
                f"Done. Add your shared files into the `{gummi.constants.TEMPLATE_FOLDER}` folder")
            return gummi.exit_code.SUCCESS
        else:
            print(
                f"There was an error. Does the `{gummi.constants.TEMPLATE_FOLDER}` folder already exist?")
            return gummi.exit_code.ALREADY

    def __ask_source(self):
        while True:
            source = input("Enter the template git repository: ")
            if rfc3987.match(source, rule='IRI'):
                break
            print(f"Please try another git repository than {source}.")
        return source

    def __clone_repo(self, source):
        try:
            g = git.Git(gummi.constants.MANAGED_FOLDER).clone(source)
        except git.exc.GitError as e:
            print(e)
            return False
        return True
