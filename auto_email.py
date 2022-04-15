import ezgmail
from netmiko import ConnectHandler
import json
import socket

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
    device = ConnectHandler(device_type='huawei', ip='x.x.x.x', username='jon_doe', password='don_joe') 
except:
    f=open('connection_log.txt','a')
    f.write("Couldn't connect to router at x.x.x.x")
    f.close()
    device = ConnectHandler(device_type='huawei', ip='x.x.x.x', username='jon_doe', password='don_joe')
device.send_command("n")    
hosts=['10.98.70.4','10.98.65.87','10.98.65.97','10.98.23.172','10.98.65.182','10.98.12.120','10.98.12.121','10.98.65.178']
links=json.load(open("router_links.json"))
#run pings
ping_test(links)
device.disconnect()

#ezgmail.init()
print("program completed") 