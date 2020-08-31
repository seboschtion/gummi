import sys
import argparse
import os
from . import exit_codes
from . import constants
from .init import run_init, run_init_template
from .detach import run_detach
from .check import run_check
from .run import run_script
from .update import run_update


def main():
    global_parser = argparse.ArgumentParser(
        prog=constants.BINARY_NAME, description=f"{constants.PROGRAM_NAME} -- Manage your LaTeX templates with ease.")
    global_parser.add_argument('-v', '--version', action='version',
                               version=version(), help="show version information and exit")

    cmd_parser = global_parser.add_subparsers(
        title='commands', dest='cmd_parser_name', help="append -h to the command to obtain more usage information")

    init_parser = cmd_parser.add_parser(
        'init', description="initialize this document for {constants.PROGRAM_NAME}")
    init_parser.add_argument('init', nargs='?', help=argparse.SUPPRESS)
    init_parser.add_argument(
        '--template', action='store_true', help="initalize a template instead")

    detach_parser = cmd_parser.add_parser(
        'detach', description=f"remove {constants.PROGRAM_NAME} configuration files")
    detach_parser.add_argument('detach', nargs='?', help=argparse.SUPPRESS)

    check_parser = cmd_parser.add_parser(
        'check', description="check for available template updates")
    check_parser.add_argument('check', nargs='?', help=argparse.SUPPRESS)

    run_parser = cmd_parser.add_parser(
        'run', description="run a script from the .scripts/ folder")
    run_parser.add_argument('run', nargs='?', help=argparse.SUPPRESS)
    run_parser.add_argument('script', metavar='script', nargs='+',
                            help="the script from the .scripts/ folder without the .sh file extension")

    update_parser = cmd_parser.add_parser(
        'update', description="update the template if necessary")
    update_parser.add_argument('update', nargs='?', help=argparse.SUPPRESS)
    update_parser.add_argument(
        '--dry', action='store_true', help="only print what would change, but do not do anything actually")
    update_parser.add_argument(
        '--retry', action='store_true', help="retry to apply the last update")

    args = global_parser.parse_args()
    if is_initialized():
        if args.cmd_parser_name == 'detach':
            return detach(detach_parser)
        if args.cmd_parser_name == 'check':
            return check(check_parser)
        if args.cmd_parser_name == 'update':
            return update(update_parser)

    if args.cmd_parser_name == 'init':
        return init(init_parser)
    if args.cmd_parser_name == 'run':
        return run(run_parser)
    print(
        f"{constants.PROGRAM_NAME} is not initialized for this document.")
    return exit_codes.NOT_INITIALIZED


def is_initialized():
    managed_folder_exists = os.path.isdir(constants.MANAGED_FOLDER)
    if not managed_folder_exists:
        return False
    repo_cloned = len(os.listdir(constants.MANAGED_FOLDER)) > 0
    return repo_cloned


def init(parser):
    args = parser.parse_args()
    if args.template:
        return run_init_template()
    elif not is_initialized():
        return run_init()
    else:
        print(
            f"{constants.PROGRAM_NAME} already initialized for this document.")
        return exit_codes.INITIALIZED


def detach(parser):
    args = parser.parse_args()
    return run_detach()


def check(parser):
    args = parser.parse_args()
    return run_check()


def run(parser):
    args = parser.parse_args()
    return run_script(args.script)


def update(parser):
    args = parser.parse_args()
    return run_update(args.dry, args.retry)


def version():
    return f"{constants.PROGRAM_NAME} version {constants.PROGRAM_VERSION}. Visit https://github.com/seboschtion/gummi for code and https://pypi.org/project/gummi/ for releases."


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nGood bye.")
        pass
