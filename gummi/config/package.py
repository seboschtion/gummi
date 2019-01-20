import gummi
from gummi.config import Base

class Package(Base):
    def __init__(self):
        super().__init__(gummi.constants.PACKAGE_CONFIG_FILENAME)

    def create(self, name, main, version):
        self.set(name, ['name'])
        self.set(main, ['main'])
        self.set(version, ['version'])
        
