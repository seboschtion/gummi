from argparse import ArgumentParser

from gummi.build import Build
from gummi.check import Check
from gummi.init import Init
from gummi.init_template import InitTemplate
from gummi.reset import Reset
from gummi.update import Update
import constants

class Program:
    def __init__(self):
        self.__commands = {'build': self.build, 'check': self.check, 'init': self.init, 'init-template': self.initTemplate, 'reset': self.reset, 'update': self.update}

    def main(self):
        args = self.get_args()
        if args.version:
            self.print_version()
            return
        if args.command == 'init' and args.init_source:
            self.__commands[args.command](args.init_source)
            return
        if args.command == 'build' and args.build_start:
            self.__commands[args.command](args.build_start)
            return
        if args.command in self.__commands.keys():
            self.__commands[args.command]()
        else:
            print("Please specify a valid command.")

    def get_args(self):
        parser = ArgumentParser(description="The Latex Docs Manager at your service!")
        commandHelp = "one of the follwing commands: " + ', '.join(self.__commands.keys())
        parser.add_argument('command', metavar='command', type=str, nargs='?', help=commandHelp)
        parser.add_argument('-v', '--version', action='store_true', help="show version information")

        # init
        parser.add_argument('--source', dest='init_source', help="source repository for template to init the doc with")

        # build
        parser.add_argument('--start', dest='build_start', help="The start file the build process should start with. You can define it in the config as well: `build -> start`.")

        return parser.parse_args()

    def build(self, start_file=None):
        build = Build()
        build.run(start_file)

    def check(self):
        check = Check()
        check.run()

    def init(self, source=None):
        init = Init()
        init.run(source)

    def initTemplate(self):
        init_template = InitTemplate()
        init_template.run()

    def reset(self):
        reset = Reset()
        reset.run()

    def update(self):
        update = Update()
        update.run()

    def print_version(self):
        print(f"{constants.PROGRAM_NAME} version {constants.PROGRAM_VERSION}")

if __name__ == '__main__':
    try:
        program = Program()
        program.main()
    except KeyboardInterrupt:
        print("\n\nGood bye.")

