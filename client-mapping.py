#!/usr/bin/env python

import argparse, string, os, sys
from netaddr import *
from unifi.controller import Controller
from python_hosts import Hosts, HostsEntry


controllerIP = os.getenv("UNIFI_CONTROLLER")
if controllerIP is None:
    controllerIP = "localhost"
print "Using controller IP %s" % controllerIP

userName = os.getenv("UNIFI_USER")
if userName is None:
    userName = raw_input('Username: ')
else:
    print "Using username %s" % userName

password = os.getenv("UNIFI_PASSWORD")
if password is None:
    password = raw_input('Password: ')

c = Controller(controllerIP, userName, password, "8443", "v4", "default")
clients = c.get_clients()
list = {}
hosts = Hosts(path='/etc/hosts')

for client in clients:
    ip = client.get('ip', 'Unknown')
    hostname = client.get('hostname')
    name = client.get('name', hostname)
    mac = client['mac']

    if ip <> "Unknown":
        ip = IPAddress(ip)

    if ip <> "Unknown" and name <> None:
        name = name.replace(" ", "")
        list[ip] = name
        sorted(list)

for entry in list.items():
    ip = str(entry[0])
    name = entry[1]
    new_entry = HostsEntry(entry_type='ipv4', address=ip, names=[name])

    if hosts.exists(ip):
      hosts.remove_all_matching(ip)

    hosts.add([new_entry])
    print entry[0],'\t',entry[1]

try:
    hosts.write()
except:
    print "You need root permissions to write to /etc/hosts - skipping!"
    sys.exit(1)


