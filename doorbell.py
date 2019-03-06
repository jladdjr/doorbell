#!/usr/bin/env python

from multiprocessing import Pool
import os
from time import sleep, time

debug = False

class State:
    def __init__(self, active=False, inactive_time=None):
        self.active = active
        self.inactive_time = inactive_time

def ping(addr):
    res = os.system('ping -c 1 -w 5 {} >/dev/null'.format(addr))
    return (addr, res)

def ping_devices(addresses):
    with Pool(10) as p:
        pings = p.map(ping, addresses)

    active_addresses = (p[0] for p in pings if p[1] == 0)
    inactive_addresses = (p[0] for p in pings if p[1] != 0)

    if debug:
        print("Active addresses:\n" + '\n'.join(active_addresses))
        if len(list(active_addresses)):
            print('\n')
        print("Inctive addresses:\n" + '\n'.join(inactive_addresses))

    return (active_addresses, inactive_addresses)

if __name__ == '__main__':
    addresses = ['192.168.1.{}'.format(i) for i in range(200,211)]

    state = {a: State(False, time()) for a in addresses}

    while(True):
        active_devices, inactive_devices = ping_devices(addresses)

        for device in inactive_devices:
            if state[device].active:
                state[device].active = False
                state[device].inactive_time = time()
                print('{} went away..'.format(device))

        for device in active_devices:
            if not state[device].active:
                state[device].active = True

                if not state[device].inactive_time:
                    note_on_timing = ""
                    time_away = 0
                else:
                    time_away = time() - state[device].inactive_time
                    note_on_timing = '(away {0} seconds)'.format(time_away)
                print('{0} came online {1}'.format(device, note_on_timing))

                if time_away > 60 * 15:
                    os.system('notify {} is home'.format(device))

        sleep(5)
