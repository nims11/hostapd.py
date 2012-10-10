# config_order specifies the attribute and their order in which the wizard processes them
config_order = ('interface', 'driver', 'ssid', 'hw_mode','ieee80211n', 'channel', 'macaddr_acl', 'auth_algs', 'ignore_broadcast_ssid', 'wpa', 'wpa_passphrase', 'wpa_key_mgmt', 'wpa_pairwise', 'rsn_pairwise')

# config_template specifies the attribute type, default value and available choices
# type 0 means that the attribute doesn't have any limited choices as their values
# type 1 means that the attribute value should be from one of the values specified by 'choices' list
config_template = {	
		'interface' : {'type' : 0, 'default' : 'wlan0'},
		'driver' : {'type' : 0, 'default' : 'nl80211'},
		'ssid' : {'type' : 0, 'default' : 'test'},
		'hw_mode' : {'type' : 1, 'default' : 'g', 'choices' : ['a','b','g']},
		'ieee80211n' : {'type' : 1, 'default' : '0', 'choices' : ['0','1']},
		'channel' : {'type' : 1, 'default' : '6', 'choices' : [str(x) for x in range(1,12)]},
		'macaddr_acl' : {'type' : 1, 'default' : '0', 'choices' : ['0','1','2']},
		'auth_algs' : {'type' : 1, 'default' : '1', 'choices' : ['1','2','3']},
		'ignore_broadcast_ssid' : {'type' : 1, 'default' : '0', 'choices' : ['0','1','2']},
		'wpa' : {'type' : 1, 'default' : '3', 'choices' : ['1','2','3']},
		'wpa_passphrase' : {'type' : 0, 'default' : 'foobar123'},
		'wpa_key_mgmt' : {'type' : 1, 'default' : 'WPA-PSK', 'choices' : ['WPA-PSK','WPA-EAP','WPA-PSK WPA-EAP']},
		'wpa_pairwise' : {'type' : 1, 'default' : 'TKIP', 'choices' : ['TKIP','CCMP']},
		'rsn_pairwise' : {'type' : 1, 'default' : 'CCMP', 'choices' : ['TKIP','CCMP']},
		}


# keys enclosed within '$' are used in the dhcp config file generation
network_settings = {
		'IN' : 'wlan0',
		'OUT' : 'eth0',
		'IP_WLAN' : '10.0.0.1',
		'$IP_ROUTER$' : '10.0.0.1',
		'$IP_NETMASK$' : '255.255.255.0',
		'$IP_SUBNET$' : '10.0.0.0',
		'$IP_BROADCAST$' : '10.0.0.255',
		'$DNS_1$' : '8.8.8.8',
		'$DNS_2$' : '8.8.4.4',
		'$IP_RANGE_MIN$' : '10.0.0.3',
		'$IP_RANGE_MAX$' : '10.0.0.12',
		}

# dhcpd_template holds the basic layout for the /etc/py_hostapd_dhcpd.conf
# variables are enclosed within '$'s
dhcpd_template =('ddns-update-style none;\n'
'ignore client-updates;\n'
'authoritative;\n'
'option local-wpad code 252 = text;\n'
'subnet\n'
'$IP_SUBNET$ netmask $IP_NETMASK$ {\n'
'option routers\n'
'$IP_ROUTER$;\n'
'option subnet-mask\n'
'$IP_NETMASK$;\n'
'option broadcast-address\n'
'$IP_BROADCAST$;\n'
'option domain-name\n'
'"localhost";\n'
'option domain-name-servers\n'
'$IP_ROUTER$, $DNS_1$, $DNS_2$;\n'
'option time-offset\n'
'0;\n'
'range $IP_RANGE_MIN$ $IP_RANGE_MAX$;\n'
'default-lease-time 1209600;\n'
'max-lease-time 1814400;\n'
'}\n')
