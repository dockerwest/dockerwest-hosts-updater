import argparse
import mmap
import fileinput
import docker

from DockerWestHosts.command.base import CommandBase


class WatchDockerEvents(CommandBase):

    def __init__(self, name, version, description, args):
        self.__name = name
        self.__version = version
        self.__description = description + " watch"
        self.__file = '/etc/hosts'
        self.__ip = None

        self.__start_marker = '## START %s' % self.__name
        self.__end_marker = '## END %s' % self.__name

        self.__client = docker.from_env()
        self.__apiclient = docker.APIClient()

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
            self.__file = flags.file

        if None is not flags.ip:
            self.__ip = flags.ip

    def run(self):
        ip = 'dynamic'
        if None is not self.__ip:
            ip = self.__ip

        print(self.__description)
        print('watching docker events and update hosts with: %s' % ip)

        # check the hosts file for dockerwest markers
        self.__markers()

        # before listening to events list the currently running containers
        self.__hosts()

        # listen to events and update hosts
        self.__listen_for_events()

    def __markers(self):
        if not self.__check_markers():
            with open(self.__file, 'a') as hostsfile:
                hostsfile.write('%s\n' % self.__start_marker)
                hostsfile.write('%s\n' % self.__end_marker)

    def __check_markers(self):
        with open(self.__file, 'rb', 0) as file, \
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(str.encode(self.__start_marker)) != -1:
                return True

        return False

    def __listen_for_events(self):
        while True:
            for event in self.__client.events(decode=True):
                self.__handleevent(event)
                break

    def __handleevent(self, event):
        if 'status' in event and \
                (
                    'start' == event['status']
                    or 'stop' == event['status']
                    or 'kill' == event['status']
                    or 'die' == event['status']
                ):
            self.__hosts()

    def __hosts(self):
        hosts = []
        containers = self.__client.containers.list()
        for container in containers:
            if 'running' == container.status:
                hostsinfo = self.__hostsinfo(container)
                if None is not hostsinfo:
                    hosts += [hostsinfo]

        self.__update_hosts(hosts)

    def __hostsinfo(self, container):
        hosts = []
        ips = []
        container_info = self.__apiclient.inspect_container(container.name)
        if "Config" in container_info and "Env" in container_info["Config"]:
            for envvar in container_info["Config"]["Env"]:
                envvarkey, envvarvalue = envvar.split("=")
                if "VIRTUAL_HOST" == envvarkey or "DOMAIN_NAME" == envvarkey:
                    hosts += envvarvalue.split(',')
        if hosts:
            if None is self.__ip:
                if "NetworkSettings" in container_info:
                    container_nwsettings = container_info["NetworkSettings"]
                    if "IPAddress" in container_nwsettings \
                            and "" != container_nwsettings["IPAddress"]:
                        ips += [container_nwsettings["IPAddress"]]
                    if "Networks" in container_nwsettings:
                        nwnetworks = container_nwsettings["Networks"]
                        for nwname, nwsettings in nwnetworks.items():
                            if "IPAddress" in nwsettings \
                                    and "" != nwsettings["IPAddress"]:
                                ips += [nwsettings["IPAddress"]]
            else:
                ips += [self.__ip]

            if ips:
                return [ips, hosts]
            else:
                return None
        return None

    def __update_hosts(self, hosts):
        hostslines = []
        for host in hosts:
            for ip in host[0]:
                line = "%s %s" % (ip, " ".join(host[1]))
                hostslines += [line]

        hostslinesstr = "\n".join(hostslines)

        inblock=False
        for line in fileinput.input(self.__file, inplace=True):
            checkline = line.rstrip()
            if self.__end_marker == checkline:
                inblock=False

            if True is inblock:
                checkline = ''

            if self.__start_marker == checkline:
                inblock=True
                checkline += "\n%s" % hostslinesstr

            if '' != checkline:
                print(checkline)
