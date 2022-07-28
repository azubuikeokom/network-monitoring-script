from netmiko import ConnectHandler
from datetime import date, time
import json
import os ,time

#Enter router/switch credentials for backup
def create_node_details():
    print("Welcome!\n What do you wish to configure for backup?\n 1.Router\n 2.Switch")
    int_choice=input()
    node_name=input('Enter router/switch name')
    node_ip=input("Enter IP of host")
    node_username=input("Enter host Username")
    node_passord=input("Enter Password")
    node_upLink_router_ip=input("Enter uplink router IP")
"""def is_ip(ip):
    #do ip test with regex"""

#define backup function
def run_backup(node_list):
    #get dict of each router-switch
    node_count=0
    for node in node_list:
        #loops through the keys of the node to return router/switch name
        for router_name in node.keys():
            #loads and return router/switch object-dictionary from the jSON 
            node_details=node[router_name]
            #connect to device
            device=ConnectHandler(device_type='huawei', ip=node_details['ip'], username=node_details['username'], password=node_details['password'], timeout=60)
            current_config=device.send_command("display cur")
            try:
                f=open(today+"/"+router_name,'w')
                f.write(current_config)
            except:
                print("can not create file")
            finally:
                f.close()
                print('Backup of %s completed!'%router_name)
            device.disconnect()
            time.sleep(2)
        #to damp connection shock    
        node_count=node_count+1
        if node_count==10:
            time.sleep(30)
#list of json files of devices to backup


"""program starts here"""
with open("routers.json") as f:
    global node_list
    node_list=json.load(f)["routers"]
    
today=str(date.today())
#create directory to store backup with today's date
os.mkdir(today)
run_backup(node_list)
        


