# Import required modules/packages/library
import pexpect
from pprint import pprint
import re
# Display heading
print('')
print('Interfaces, routes list, routes details')
print('---------------------------------------')

# Create regular expressions to match interfaces and OSPF
OSPF_pattern = re.compile(r'O.+')
intf_pattern = re.compile(r'(GigabitEthernet)(\d)')

# Create regular expressions to match prefix and routes
prefix_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/?\d?\d?)')
route_pattern = re.compile(r'via (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Connect to device and run 'show ip route' command
print('--- connecting telnet 192.168.56.130 with prne/cisco123!')

session = pexpect.spawn('telnet 192.168.56.130', encoding='utf-8', timeout=20)
result = session.expect(['Username:', pexpect.TIMEOUT, pexpect.EOF])

# Check for failure
if result != 0:
    print('Timeout or unexpected reply from device')
    exit()
# Enter username
session.sendline('prne')
result = session.expect('Password:')

# Enter password
session.sendline('cisco123!')
result = session.expect('>')

# Must set terminal length to zero for long replies, no pauses
print('--- setting terminal length to 0')
session.sendline('terminal length 0')
result = session.expect('>')

# Run the 'show ip route' command on device
print('--- successfully logged into device, running show ip route command')
session.sendline('show ip route')
result = session.expect('>')

# Display the output of the command, for comparison
print('--- show ip route output:')
show_ip_route_output = session.before
print(show_ip_route_output)

# Get the output from the command into a list of lines from the output
routes_list = show_ip_route_output.splitlines()
# Create dictionary to hold number of routes per interface
ospf_info = {'router_id': None, 'areas': []}
# Run the 'show ip ospf command on the device
print('--- running show ip ospf command')
session.sendline('show ip ospf')
result = session.expect('>')
# Display the output of the command, for comparison
print('--- show ip ospf output:')
show_ip_ospf_output = session.before
print(show_ip_route_output)
# Extract OSPF router ID
router_id_match = re.search(r'Router ID (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
if router_id_match:
    ospf_info['router_id'] = router_id_match.group(1)
# Extract ospf area information
area_matches = re.finditer(r'Area (\d+)',)
for match in area_matches:
    ospf_info['areas'].append(match.group(1))
# Create a dictionary to hold the number of routers per interface
intf_routers = {}        
# Go through the list of routes to get routes per interface
for route in  routes_list:

    OSPF_match = OSPF_pattern.search(route)
    if OSPF_match:

        # Match for GigabitEthernet interfaces
        intf_match = intf_pattern.search(route) 
        
        # Check to see if we matched the GigabitEthernet interfaces string
        if intf_match:

            # Get the interfaces from the match
            intf = intf_match.group(2)

            # If route list not yet created, do so now
            if intf not in ospf_info:
                ospf_info[intf] = []

                # Exract the prefix (destination IP address/subnet)
            prefix_match = prefix_pattern.search(route)
            prefix = prefix_match.group(1)

                # Extract the route
            route_match = route_pattern.search(route)
            next_hop = route_match.group(1)

                # Create dictionary for this this route,
                # and add it to the list
            route = {'prefix': prefix, 'next-hop': next_hop}
            ospf_info[intf].append(route)


# Display a blank line to make easier to read
print('')

# Display a title
print('OSPF routes out of GigabitEthernet interfaces:')

# Display the GigabitEthernet interfaces routes
pprint(ospf_info)

# Display a blank line to make easier to read
print('')
# Close the file
#file.close()
