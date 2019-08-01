import argparse

from DockerWestHosts.version import __version__
from DockerWestHosts.command.watch import WatchDockerEvents


class HostsUpdater:

    def __init__(self):
        self.__name = "dockerwest-hosts-updater"
        self.__version = __version__
        self.__description = (
            "DockerWest Hosts Updater (%s)"
            % (__version__)
        )

        self.__command_map = {
            'watch': WatchDockerEvents
        }

        self.__parser = argparse.ArgumentParser(
            description=self.description(),
            prog=self.name()
        )
        self.__parser.add_argument('command', choices=self.__command_map)
        self.__parser.add_argument(
            '--debug',
            required=False,
            action='store_true',
            help='enable debugging (stacktraces on errors)'
        )
        self.__parser.add_argument(
            'command_args',
            nargs=argparse.REMAINDER,
            help='use help of subcommand for more info'
        )

    def name(self):
        return self.__name

    def version(self):
        return self.__version

    def description(self):
        return self.__description

    def run(self):
        args = self.__parser.parse_args()

        if True is args.debug:
            command_class = self.__command_map[args.command]
            command = command_class(
                self.__name,
                self.__version,
                self.__description,
                args.command_args
            )
            command.run()
        else:
            try:
                command_class = self.__command_map[args.command]
                command = command_class(
                    self.__name,
                    self.__version,
                    self.__description,
                    args.command_args
                )
                command.run()
            except Exception as e:
                print(e)

