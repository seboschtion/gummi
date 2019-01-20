import gummi.constants as constants
import gummi.exit_code as exit_code
from gummi.config import DocumentConfig
from gummi.filesystem import Filesystem

class Init():
    def __init__(self):
        self.doc_config = DocumentConfig()
        self.filesystem = Filesystem()

    def run(self):
        if self.doc_config.exists():
            print(f"{constants.PROGRAM_NAME} already initialized for this document.")
            return exit_code.ALREADY
        self.create_config()
        self.create_filestructure()
        print("The document is now initialized, happy typing!")
        return exit_code.SUCCESS

    def create_config(self):
        self.doc_config.create()

    def create_filestructure(self):
        if not self.filesystem.is_initialized():
            self.filesystem.init()

