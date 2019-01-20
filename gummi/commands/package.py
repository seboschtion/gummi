import os

import gummi
import gummi.config

class Package():
    def __init__(self):
        self.package_config = gummi.config.Package()

    def create(self):
        if self.package_config.exists():
            print("This folder already holds a package.")
            return gummi.exit_code.ALREADY
        name, main, version = self.__get_package_user_info()
        self.package_config.create(name, main, version)
        return gummi.exit_code.SUCCESS

    def __get_package_user_info(self):
        default_name = os.path.split(os.getcwd())[-1]
        name = input(f"Enter the name of your package [{default_name}]: ")
        if name is '': name = default_name
        while True:
            main = input("Provide the name of your main .tex file: ")
            if main is not '': break
        default_version = "1.0"
        version = input(f"Package version [{default_version}]: ")
        if version is '': version = default_version
        return name, main, version

