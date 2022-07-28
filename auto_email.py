import ezgmail
from netmiko import ConnectHandler
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv() 
def ping_test(link_maps):
    reachable=set()
    not_reachable=set()
    for ip in link_maps.keys():
        #send ping from router to ip 
        output = device.send_command("ping -c 4 -m 10 %s" % ip) 
        if "100.00%" not in output:
            reachable.add(link_maps[ip])
        else:
            not_reachable.add(link_maps[ip])

    #convert list to strng and use carriage return as delimiters        
    reachable='\n'.join(reachable)    
    not_reachable='\n'.join(not_reachable)     
    #print("The following links are currently UP:\n {}".format(reachable))
    print("The following links are currently DOWN:\n {}".format(not_reachable))

    #send email of link status
    ezgmail.send("azubuikeokom@gmail.com","Network report",
    "The following links are currently DOWN:\n {}".format(not_reachable))
    

def config_link(hosts,links):
    host=input("Enter host ip")
    link_ip=input("Enter ip of link")
    link_name=input("Enter name of link eg 10G NNE003 to ONT009")
    hosts.append(host)
    links[link_ip]=link_name

"""program starts here"""
#connect to router via ssh
try:
    device = ConnectHandler(device_type='huawei', ip=os.getenv('public_ip'), username=os.getenv('myusername'), password=os.getenv('public_password')) 
except:
    f=open('connection_log.txt','a')
    f.write("\nCouldn't connect to router at {} at {} ".format(datetime.now(),os.getenv('public_ip')) )
    f.close()
    device = ConnectHandler(device_type='huawei', ip=os.getenv('private_ip'), username=os.getenv('myusername'), password=os.getenv('private_password'))
device.send_command("n")    
links=json.load(open("router_links.json"))
#run pings
ping_test(links)
device.disconnect()

#ezgmail.init()
#print("program completed") 