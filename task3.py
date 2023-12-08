import netmiko

# Define the router credentials
router1_ip = '192.168.56.101'
router1_username = 'cisco'
router1_password = 'cisco'

router2_ip = '192.168.56.130'
router2_username = 'cisco'
router2_password = 'cisco'

# Define the OSPF configuration commands
loopback_config = 'interface loopback 0\n ip address 10.1.1.1 255.255.255.0\n interface GigabitEthernet0/0\n ip address 192.168.56.101 255.255.255.255\n no shutdown\n'
router_ospf_config = 'router ospf 1\n network 192.168.56.101 0.0.0.0 area 0\n network 10.1.1.0 0.0.0.255 area 0'

# Connect to the routers
router1 = netmiko.ConnectHandler(device_type='cisco_ios', ip=router1_ip, username=router1_username, password=router1_password)
router2 = netmiko.ConnectHandler(device_type='cisco_ios', ip=router2_ip, username=router2_username, password=router2_password)

# Configure the loopback interface and OSPF on Router 1
router1.send_config_set(loopback_config + router_ospf_config)

# Configure the loopback interface and OSPF on Router 2
router2.send_config_set(loopback_config + router_ospf_config)

# Close the connections to the routers
router1.disconnect()
router2.disconnect()
