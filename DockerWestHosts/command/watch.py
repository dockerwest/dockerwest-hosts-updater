import argparse
import docker

from DockerWestHosts.command.base import CommandBase


class WatchDockerEvents(CommandBase):

    def __init__(self, name, version, description, args):
        self.__name = name
        self.__version = version
        self.__description = description + " watch"
        self.__file = '/etc/hosts'
        self.__ip = None

        parser = argparse.ArgumentParser(
            description=self.__description,
            prog=self.__name
        )
        parser.add_argument(
            '--file',
            required=False,
            help='specify file to update (default: /etc/hosts)'
        )
        parser.add_argument(
            '--ip',
            required=False,
            help='set fixed ip - for docker machine or docker desktop'
        )

        flags = parser.parse_args(args)

        if None is not flags.file:
            self.__file = args.file

        if None is not flags.ip:
            self.__ip = args.ip

    def run(self):
        ip = 'dynamic'
        if None is not self.__ip:
            ip = self.__ip

        print(self.__description)
        print('watching docker events and update hosts with: %s' % ip)
        client = docker.from_env()
        while True:
            for event in client.events(decode=True):
                self.handleevent(event)
                break

    def handleevent(self, event):
        if 'status' in event and \
                (
                    'start' == event['status']
                    or 'stop' == event['status']
                    or 'kill' == event['status']
                    or 'die' == event['status']
                ):
            print(event)
