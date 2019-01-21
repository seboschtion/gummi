import sys
import argparse

import gummi
import gummi.commands

class Program:
    def main(self):
        global_parser = argparse.ArgumentParser(prog=gummi.constants.BINARY_NAME, description=f"{gummi.constants.PROGRAM_NAME} - manage your LaTeX templates with ease")
        global_parser.add_argument('-v', '--version', action='version', version=self.version(), help="show version information and exit")
        cmd_parser = global_parser.add_subparsers(title='commands', dest='cmd_parser_name', help="append -h to the command to obtain more usage information")

        init_parser = cmd_parser.add_parser('init', description="initialize this document for {}".format(gummi.constants.PROGRAM_NAME))
        init_parser.add_argument('init', nargs='?', help=argparse.SUPPRESS)
        detach_parser = cmd_parser.add_parser('detach', description="remove {} configuration files".format(gummi.constants.PROGRAM_NAME))
        detach_parser.add_argument('detach', nargs='?', help=argparse.SUPPRESS)
        check_parser = cmd_parser.add_parser('check', description="check for available template updates")
        check_parser.add_argument('check', nargs='?', help=argparse.SUPPRESS)
        update_parser = cmd_parser.add_parser('update', description="update the template if necessary")
        update_parser.add_argument('update', nargs='?', help=argparse.SUPPRESS)

        args = global_parser.parse_args()
        doc_initialized = gummi.util.Files().is_initialized()
        if doc_initialized:
            if args.cmd_parser_name == 'detach': return self.detach(detach_parser)
            if args.cmd_parser_name == 'check': return self.check(check_parser)
            if args.cmd_parser_name == 'update': return self.update(update_parser)
            print(f"{gummi.constants.PROGRAM_NAME} already initialized for this document.")
            return gummi.exit_code.INITIALIZED
        if not doc_initialized: 
            if args.cmd_parser_name == 'init': return self.init(init_parser)
            print(f"{gummi.constants.PROGRAM_NAME} is not initialized for this document.")
            return gummi.exit_code.NOT_INITIALIZED
        return gummi.exit_code.COMMAND_INTERPRETATION

    def init(self, parser):
        args = parser.parse_args()
        return gummi.commands.Init().run()

    def detach(self, parser):
        args = parser.parse_args()
        return gummi.commands.Detach().run()

    def check(self, parser):
        args = parser.parse_args()
        return gummi.commands.Check().run(quiet=False)

    def update(self, parser):
        args = parser.parse_args()
        return gummi.commands.Update().run()

    def version(self):
        return "{} version {}\nmore on https://github.com/latex-gummi/gummi".format(gummi.constants.PROGRAM_NAME, gummi.constants.PROGRAM_VERSION)

if __name__ == '__main__':
    try:
        program = Program()
        sys.exit(program.main())
    except KeyboardInterrupt:
        print("\n\nGood bye.")

