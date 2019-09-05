DockerWest hosts updater
========================

Automatic updating of your hosts file based on your running docker containers.

There is one prerequisite, the evironment variable `VIRTUAL_HOST` or
`DOMAIN_NAME` must be set in your running container to give it an entry in your
hosts file.

## requirements

- python3
- python3 setuptools

## installation

``` sh
sudo python3 setup.py install
```

Then you end up with `/usr/bin/dockerwest-hosts-updater`

## usage

``` sh
usage: dockerwest-hosts-updater [-h] [--debug] {watch} ...

DockerWest Hosts Updater (0.0.dev)

positional arguments:
  {watch}
  command_args  use help of subcommand for more info

optional arguments:
  -h, --help    show this help message and exit
  --debug       enable debugging (stacktraces on errors)
```

``` sh
usage: dockerwest-hosts-updater [-h] [--file FILE] [--ip IP]

DockerWest Hosts Updater (0.0.dev) watch

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  specify file to update (default: /etc/hosts)
  --ip IP      set fixed ip - for docker machine or docker desktop
```

If you just run `dockerwest-hosts-updater watch` it will start watching for
docker events and update your /etc/hosts file based on that information. Since
`/etc/hosts` is being update you need sufficient privileges to edit that file.

If you have docker running on a remote machine with a proxy or something you
can pass along the `--ip` flag so your hosts file will be updated accordingly
(for example when you are using dinghy).

If your hosts file is not found on the default location, you can also give the
`--file` flag to point to the location your system has the hosts file on.

## systemd service

After installation you can copy the systemd service from the contrib folder to
`/etc/systemd/system/` to allow the hosts updater to run on system startup.

``` sh
sudo cp contrib/dockerwest-hosts-updater.service /etc/systemd/system/
sudo systemctl enable dockerwest-hosts-updater.service
sudo systemctl start dockerwest-hosts-updater.service
```

## contributing

Have an issue, questions, improvements, ... open an issue on github, or even
better create a pull request.
