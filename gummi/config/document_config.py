import gummi.constants as constants
from gummi.config.config_base import ConfigBase

class DocumentConfig(ConfigBase):
    def __init__(self):
        super().__init__(constants.CONFIG_FILENAME)

    def create(self):
        self.set([], ["packages"])
        self.set({}, ["template"])

