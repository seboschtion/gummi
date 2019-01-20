import gummi
import gummi.util
import gummi.config

class Init():
    def __init__(self):
        self.doc_config = gummi.config.Document()
        self.files = gummi.util.Files()

    def run(self):
        if self.doc_config.exists():
            print(f"{gummi.constants.PROGRAM_NAME} already initialized for this document.")
            return gummi.exit_code.ALREADY
        self.__create_config()
        self.__create_filestructure()
        print("The document is now initialized, happy typing!")
        return gummi.exit_code.SUCCESS

    def __create_config(self):
        self.doc_config.create()

    def __create_filestructure(self):
        if not self.files.is_initialized():
            self.files.init()

