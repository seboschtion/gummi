from pathlib import Path
from subprocess import call
from . import exit_codes


def run_script(script):
    scriptpath = Path(f".scripts/{script}.sh")
    if scriptpath.exists():
        with open(scriptpath.absolute(), 'rb') as scriptfile:
            scriptbinary = scriptfile.read()
            result = call(scriptbinary, shell=True)
        return result
    return exit_codes.SCRIPT_NOT_FOUND
