from getpass import getpass
from netmiko import ConnectHandler

username = 'prne'
ip = '192.168.56.101'
password = 'cisco123!'
secret = 'class123!'


with  open('commands_file.txt') as f:
    commands_list = f.read().splitlines()

with open('devices_file.txt') as f:
    devices_list = f.read().splitlines() 

for devices in devices_list:
    print('Connecting to device" ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type' : 'cisco_ios',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_config_set(commands_list)
    print(output)       