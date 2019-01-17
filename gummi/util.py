import os

import constants
from gummi.config import Config

def remove_dotpath(path):
    config = Config()
    dotpath = os.path.join(constants.MANAGED_FOLDER, config.get_source_name(), constants.TEMPLATE_FOLDER)
    path = path.replace(dotpath, '')
    if path.find('/') == 0:
        path = path[1:]
    if path == '':
        path = '.'
    return path

