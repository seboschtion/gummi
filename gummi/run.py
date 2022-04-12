import stat
from pathlib import Path
from os import access, R_OK, X_OK
from subprocess import call
from . import exit_codes


def run_script(script):
    scriptname = script[0]
    scriptpath = Path(f".scripts/{scriptname}.sh")
    script[0] = scriptpath.absolute()
    if scriptpath.exists():
        try:
            if not access(script[0], R_OK | X_OK):
                print(f"Trying to set permissions of {script[0]}")
                scriptpath.chmod(scriptpath.stat().st_mode | stat.S_IRUSR | stat.S_IXUSR)
            return call(script)
        except:
            print(f"The {script[0]} is not executeable.")
            return exit_codes.SCRIPT_NOT_EXECUTEABLE
    print(f"The script {scriptname} was not found in {script[0]}.")
    return exit_codes.SCRIPT_NOT_FOUND
