import gummi.constants as constants
from gummi.config.config_base import ConfigBase

class PackageConfig(ConfigBase):
    def __init__(self):
        super().__init__(constants.PACKAGE_CONFIG_FILENAME)

    def create(self, name, main, version):
        self.set(name, ['name'])
        self.set(main, ['main'])
        self.set(version, ['version'])
        
