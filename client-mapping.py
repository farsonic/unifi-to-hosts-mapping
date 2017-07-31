#!/usr/bin/env python

import argparse, string, os, sys
from netaddr import *
from unifi.controller import Controller
from python_hosts import Hosts, HostsEntry

parser = argparse.ArgumentParser(description = "Fetch list of hosts from unifi controller and place them in a hosts file")
parser.add_argument('-v', '--verbose', action='store_true', help = "print additional information")

parser.add_argument('-nh', '--nohosts', action='store_true', help = "don't attempt to write to hosts file")
parser.add_argument('-m', '--mixedcase', action='store_true', help = "do not force all names to lower case")

parser.add_argument('-f', '--hostfile', help = "hosts file to use", default = "/etc/hosts")
parser.add_argument('-c', '--controller', help = "controller IP or hostname")
parser.add_argument('-u', '--user', help = "username")
parser.add_argument('-p', '--password', help = "password")
args = parser.parse_args()

if args.verbose:
    print args

if args.controller is not None:
    controllerIP = args.controller
else:
    controllerIP = os.getenv("UNIFI_CONTROLLER")
    if controllerIP is None:
        controllerIP = raw_input('Controller: ')
if args.verbose:
    print "Using controller IP %s" % controllerIP

if args.user is not None:
    userName = args.user
else:
    userName = os.getenv("UNIFI_USER")
    if userName is None:
        userName = raw_input('Username: ')
if args.verbose:
    print "Using username %s" % userName

if args.password is not None:
    password = args.password
else:
    password = os.getenv("UNIFI_PASSWORD")
    if password is None:
        password = raw_input('Password: ')

c = Controller(controllerIP, userName, password, "8443", "v4", "default")
clients = c.get_clients()
list = {}

if args.verbose:
    print "Using hosts file %s" % args.hostfile
hosts = Hosts(path=args.hostfile)

for client in clients:
    ip = client.get('ip', 'Unknown')
    hostname = client.get('hostname')
    name = client.get('name', hostname)
    if not args.mixedcase:
        name = name.lower()
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
    if args.verbose:
        print entry[0],'\t',entry[1]

if args.verbose:
    if args.nohosts:
        print "--nohosts specified, not attempting to write to hosts file"

if not args.nohosts:
    try:
        hosts.write()
    except:
        print "You need root permissions to write to /etc/hosts - skipping!"
        sys.exit(1)
