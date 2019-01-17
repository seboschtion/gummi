import os
from pathlib import Path
from subprocess import call

import constants
from gummi.config import Config

class Build:
    def __init__(self):
        self.config = Config()
        return

    def run(self, start_file=None):
        print("build is not implemented yet.")
        self.prepare_folder()
        error = self.build(start_file)
        self.cleanup()
        if error:
            print("There was an error building the project.")

    def prepare_folder(self):
        try:
            os.mkdir(constants.BUILD_PATH)
        except OSError:
            pass

    def build(self, start_file):
        start_file = self.get_start_file(start_file)
        if not isinstance(start_file, str) or not os.path.isfile(start_file):
            print("The start file is corrupt or not given.")
            return False
        exitcode = call(['pdflatex', '-output-directory', constants.BUILD_PATH, start_file])
        return exitcode == 0

    def get_start_file(self, start_file):
        if start_file:
            return start_file
        from_config = self.config.get_build_start()
        if not from_config:
            print("No start file given, add one to your config or append it to the build command. Use -h for more information.")
            return None
        return from_config
        
    def cleanup(self):
        path = constants.BUILD_PATH
        files = list(Path(path).rglob('*[!.pdf]'))
        for file in files:
            os.remove(file)

