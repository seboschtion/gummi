import sys
from argparse import ArgumentParser, SUPPRESS

import gummi.constants as constants
import gummi.exit_code as exit_code
from gummi.init import Init
from gummi.detach import Detach
from gummi.package import PackageAdmin

class Program:
    def main(self):
        global_parser = ArgumentParser(prog=constants.BINARY_NAME, description=f"{constants.PROGRAM_NAME} - your LaTeX document management tool.")
        global_parser.add_argument('-v', '--version', action='version', version=self.version(), help="show version information and exit")
        cmd_parser = global_parser.add_subparsers(title='commands', dest='cmd_parser_name', help="append -h to the command to obtain more usage information")

        init_parser = cmd_parser.add_parser('init', description="initialize this document for {}".format(constants.PROGRAM_NAME))
        init_parser.add_argument('init', nargs='?', help=SUPPRESS)
        detach_parser = cmd_parser.add_parser('detach', description="remove {} configuration files".format(constants.PROGRAM_NAME))
        detach_parser.add_argument('detach', nargs='?', help=SUPPRESS)
        package_parser = cmd_parser.add_parser('package', description="create and manage a custom built {} package".format(constants.PROGRAM_NAME))
        package_parser.add_argument('package', nargs='?', help=SUPPRESS)
        package_parsers = package_parser.add_subparsers(title='subcommands', dest='package_parser_name', help="append -h to the command to obtain more usage information")
        package_parsers.add_parser('create', description="create a {} package".format(constants.PROGRAM_NAME))

        args = global_parser.parse_args()
        if args.cmd_parser_name == 'init': return self.init(init_parser)
        elif args.cmd_parser_name == 'detach': return self.detach(detach_parser)
        elif args.cmd_parser_name == 'package': return self.package(package_parser)
        global_parser.print_help()
        return exit_code.COMMAND_INTERPRETATION

    def init(self, parser):
        args = parser.parse_args()
        return Init().run()

    def detach(self, parser):
        args = parser.parse_args()
        return Detach().run()

    def package(self, parser):
        args = parser.parse_args()
        admin = PackageAdmin()
        if args.package_parser_name == 'create':
            return admin.create()

    def version(self):
        return "{} version {}".format(constants.PROGRAM_NAME, constants.PROGRAM_VERSION)

if __name__ == '__main__':
    try:
        program = Program()
        sys.exit(program.main())
    except KeyboardInterrupt:
        print("\n\nGood bye.")

