import argparse

from DockerWestHosts.command.base import CommandBase


class WatchDockerEvents(CommandBase):

    def __init__(self, name, version, description, args):
        self.__name = name
        self.__version = version
        self.__description = description + " watch"
        self.__args = args

        self.__parser = argparse.ArgumentParser(
            description=self.__description,
            prog=self.__name
        )
        self.__parser.add_argument(
            '--file',
            required=False,
            help='specify file to update (default: /etc/hosts)'
        )
        self.__parser.add_argument(
            '--ip',
            required=False,
            help='set fixed ip - for docker machine or docker desktop'
        )

    def run(self):
        args = self.__parser.parse_args(self.__args)
        print(args)
