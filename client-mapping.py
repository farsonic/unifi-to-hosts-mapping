#!/usr/bin/env python

import argparse,string
from netaddr import *
from unifi.controller import Controller
from python_hosts import Hosts, HostsEntry

c = Controller("ip-address", "username", "password", "8443", "v4", "default")
clients = c.get_clients()
list = {}
hosts = Hosts(path='/etc/hosts')

for client in clients:
    ip = client.get('ip', 'Unknown')
    name = client.get('name')
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
   
hosts.write()
    