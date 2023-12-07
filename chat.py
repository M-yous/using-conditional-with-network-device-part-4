from ncclient import manager


def main():
    """
    Main method that prints netconf capabilities of device.
    """

    device = {"ip": "10.2.100.11", "port": "830", "platform": "csr",}

    with manager.connect(host=device['ip'], port=device['port'], username='admin',
                         password='cisco.123', hostkey_verify=False,
                         device_params={'name': device['platform']},
                         look_for_keys=False, allow_agent=False) as m:

        rpc = '''
                <config>
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <router>
                            <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
                                <id>100</id>
                                <router-id>1.1.1.1</router-id>
                                <network>
                                    <ip>10.1.1.0</ip>
                                    <mask>0.0.0.3</mask>
                                    <area>0</area>
                                </network>
                            </ospf>
                        </router>
                    </native>
                </config>
            '''

        reply = m.edit_config(rpc, target='running')
        print(reply)


if __name__ == '__main__':
    main()
