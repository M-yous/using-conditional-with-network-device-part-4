from getpass import getpass
from netmiko import ConnectHandler

username = 'prne'
password = getpass('Enter password: ')
secret = 'class123!'

with open('commands_file.txt') as f:
    commands_list = f.read().splitlines()

with open('devices_file.txt') as f:
    devices_list = f.read().splitlines()

for device_ip in devices_list:
    print('Connecting to device: ' + device_ip)
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': device_ip,
        'username': username,
        'password': password,
        'secret': secret,
    }

    try:
        net_connect = ConnectHandler(**ios_device)
        net_connect.enable()  # Enter privileged exec mode
        output = net_connect.send_config_set(commands_list)
        print(output)

        # Save configuration changes
        output = net_connect.save_config()
        print(output)

    except Exception as e:
        print(f"Failed to connect to {device_ip}. Error: {str(e)}")

    finally:
        # Disconnect from the device
        net_connect.disconnect()
