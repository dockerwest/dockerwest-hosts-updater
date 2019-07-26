#!/usr/bin/env python3

import docker


def handleevent(event):
    if 'status' in event and ('start' == event['status'] or 'stop' == event['status'] or 'kill' == event['status']):
        print(event)


def run():
    client = docker.from_env()
    while True:
        for event in client.events(decode=True):
            handleevent(event)
            break

run()
