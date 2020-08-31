import stat
from pathlib import Path
from os import chmod
from subprocess import call
from . import exit_codes


def run_script(script):
    scriptpath = Path(f".scripts/{script[0]}.sh")
    script[0] = scriptpath.absolute()
    if scriptpath.exists():
        try:
            chmod(script[0], stat.S_IRUSR | stat.S_IXUSR)
            return call(script)
        except:
            return exit_codes.SCRIPT_NOT_EXECUTABLE
    return exit_codes.SCRIPT_NOT_FOUND
