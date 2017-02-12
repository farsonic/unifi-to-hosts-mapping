### unifi-to-hosts-mapping

Within the UniFi controller you can create an alias for devices as they appear on the network. This script takes the alias entries and their corresponding IP address to maintain an corresponding list of hosts on the PiHole server. This host entry resides in /etc/hosts. 

Basic workflow is 

![Image of PiHole/UniFi Workflow](https://raw.githubusercontent.com/farsonic/unifi-to-hosts-mapping/master/PiHole-WorkFlow.png)


Place script on PiHole server, in my case this is in /home/pi. You will also need to ensure you have the relevant python libraries installed. 

```
sudo pip install python-hosts
sudo pip install unifi
sudo pip instlal netaddr

```
The script will also need to be modified to include the correct details for the IP address, Username and Password of the UniFi Controller. 

Create a suitable crontab entry for the root user, it will need to be for the root user as you are modifying the /etc/hosts file. 

```
sudo 
crontab -e 

Add the following lines to the cron file and save/exit

0,15,30,45 * * * * /home/pi/build-static-dhcp.py
```
Finally, ensure you have selected "Reverse DNS lookup" for "Top Clients" within Settings on the PiHole Server 


