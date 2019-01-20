import sys, argparse

import gummi
import gummi.commands

class Program:
    def main(self):
        global_parser = argparse.ArgumentParser(prog=gummi.constants.BINARY_NAME, description=f"{gummi.constants.PROGRAM_NAME} - your LaTeX document management tool.")
        global_parser.add_argument('-v', '--version', action='version', version=self.version(), help="show version information and exit")
        cmd_parser = global_parser.add_subparsers(title='commands', dest='cmd_parser_name', help="append -h to the command to obtain more usage information")

        init_parser = cmd_parser.add_parser('init', description="initialize this document for {}".format(gummi.constants.PROGRAM_NAME))
        init_parser.add_argument('init', nargs='?', help=argparse.SUPPRESS)
        detach_parser = cmd_parser.add_parser('detach', description="remove {} configuration files".format(gummi.constants.PROGRAM_NAME))
        detach_parser.add_argument('detach', nargs='?', help=argparse.SUPPRESS)
        package_parser = cmd_parser.add_parser('package', description="create and manage a custom built {} package".format(gummi.constants.PROGRAM_NAME))
        package_parser.add_argument('package', nargs='?', help=argparse.SUPPRESS)
        package_parsers = package_parser.add_subparsers(title='subcommands', dest='package_parser_name', help="append -h to the command to obtain more usage information")
        package_parsers.add_parser('create', description="create a {} package".format(gummi.constants.PROGRAM_NAME))

        args = global_parser.parse_args()
        if args.cmd_parser_name == 'init': return self.init(init_parser)
        elif args.cmd_parser_name == 'detach': return self.detach(detach_parser)
        elif args.cmd_parser_name == 'package': return self.package(package_parser)
        global_parser.print_help()
        return gummi.exit_code.COMMAND_INTERPRETATION

    def init(self, parser):
        args = parser.parse_args()
        return gummi.commands.Init().run()

    def detach(self, parser):
        args = parser.parse_args()
        return gummi.commands.Detach().run()

    def package(self, parser):
        args = parser.parse_args()
        package = gummi.commands.Package()
        if args.package_parser_name == 'create':
            return package.create()

    def version(self):
        return "{} version {}".format(gummi.constants.PROGRAM_NAME, gummi.constants.PROGRAM_VERSION)

if __name__ == '__main__':
    try:
        program = Program()
        sys.exit(program.main())
    except KeyboardInterrupt:
        print("\n\nGood bye.")

