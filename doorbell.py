#!/usr/bin/env python

from collections import namedtuple
from multiprocessing import Pool
import os
from time import sleep

debug = True

state = namedtuple('State', ['active', 'last_inactive'])

def ping(addr):
    res = os.system('ping -c 1 -w 5 {} >/dev/null'.format(addr))
    return (addr, res)

def ping_devices(addresses):
    """Return list of active devices"""
    with Pool(10) as p:
        pings = p.map(ping, addresses)

    active_addresses = (p[0] for p in pings if p[1] == 0)
    inactive_addresses = (p[0] for p in pings if p[1] != 0)

    if debug:
        print("Active addresses:\n" + '\n'.join(active_addresses))
        if len(list(active_addresses)):
            print('\n')
        print("Inctive addresses:\n" + '\n'.join(inactive_addresses))

    return active_addresses

if __name__ == '__main__':
    addresses = ['192.168.1.{}'.format(i) for i in range(2,4)]

    while(True):
        ping_devices(addresses)
        sleep(30)
