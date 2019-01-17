from argparse import ArgumentParser

import constants, exit_code
from gummi.init import Init
from gummi.detach import Detach

class Program:
    def __init__(self):
        self.create_commands()

    def main(self):
        args = self.get_args()
        if args.version:
            self.print_version()
            return
        if args.help:
            self.print_help(args.command)
            return
        if args.command == 'init':
            return self.init()
        if args.command == 'detach':
            return self.detach()
        else:
            self.print_help(args.command)
            return exit_code.COMMAND_INTERPRETATION

    def get_args(self):
        self.parser = ArgumentParser(description=f"{constants.PROGRAM_NAME} - your LaTeX document management tool.", add_help=False)
        self.parser.add_argument('command', metavar='command', type=str, nargs='?', help=', '.join(self.commands.keys()) + " (help for each command with command and applied -h)")
        self.parser.add_argument('-h', '--help', action='store_true', help="get help")
        self.parser.add_argument('-v', '--version', action='store_true', help="show version information")
        return self.parser.parse_args()

    def init(self):
        init = Init()
        return init.run()

    def detach(self):
        reset = Detach()
        return reset.run()

    def print_version(self):
        print(f"{constants.PROGRAM_NAME} version {constants.PROGRAM_VERSION}")

    def create_commands(self):
        self.commands = {
            'detach': "remove {} configuration files".format(constants.PROGRAM_NAME),
            'init': "initialize this document for {}".format(constants.PROGRAM_NAME),
        }

    def print_help(self, command):
        if command == None:
            self.parser.print_help()
        elif command in self.commands.keys():
            print(f"{command}: {self.commands[command]}")
        else:
            print(f"Please specify a valid command. Find help by running `{constants.BINARY_NAME} -h`.")

if __name__ == '__main__':
    try:
        program = Program()
        sys.exit(program.main())
    except KeyboardInterrupt:
        print("\n\nGood bye.")

