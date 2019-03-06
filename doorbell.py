#!/usr/bin/env python

from multiprocessing import Pool
import os

def ping(addr):
    res = os.system('ping -c 1 -w 5 {} >/dev/null'.format(addr))
    return (addr, res)

if __name__ == '__main__':
    addresses = ['192.168.1.{}'.format(i) for i in range(200,211)]
    with Pool(10) as p:
        pings = p.map(ping, addresses))

    active_addresses = (p[0] for p in pings if p[1] == 0)
    print(active_addresses)
