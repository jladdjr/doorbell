#!/usr/bin/env python

from multiprocessing import Pool
import os
from time import sleep, time

debug = False

address_to_name_map = {'192.168.1.2': 'Jim',
                       '192.168.1.3': 'Stephanie'}

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

def get_identity(address):
    return address_to_name_map.get(address, address)

if __name__ == '__main__':
    addresses = ['192.168.1.{}'.format(i) for i in range(2,4)]

    state = {a: State(False, time()) for a in addresses}
    last_check = time()
    def initialize_state():
        for a in addresses:
            state[a] = State(False, time())

    initialize_state()
    while(True):
        active_devices, inactive_devices = ping_devices(addresses)
        if time() - last_check > 60:
            # reset times
            initialize_state()
            print('Resuming checks after sleep.. \o/')
            last_check = time()
            continue
        last_check = time()

        for device in inactive_devices:
            if state[device].active:
                state[device].active = False
                state[device].inactive_time = time()
                print('{} went away..'.format(get_identity(device)))

        for device in active_devices:
            if not state[device].active:
                state[device].active = True

                if not state[device].inactive_time:
                    note_on_timing = ""
                    time_away = 0
                else:
                    time_away = (time() - state[device].inactive_time) // 60  # In minutes
                    note_on_timing = '(away {0} minutes)'.format(time_away)
                print('{0} came online {1}'.format(get_identity(device), note_on_timing))

                if time_away > 20:
                    os.system('notify {} is home'.format(get_identity(device)))
                    os.system('text_steph')
                    os.system('text_jim')

        sleep(5)
