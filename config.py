# File locations
file_hostapd = '/etc/py_hostapd.conf'
file_dhcpd = '/etc/py_dhcpd.conf'
file_cfg = '/etc/py_hostapd.cfg'

# Executable locations
hostapd_path = '/usr/bin/hostapd'
dhcpd_path = '/usr/sbin/dhcpd'
ifconfig_path = '/sbin/ifconfig'
iptables_path = '/usr/sbin/iptables'
sysctl_path = '/sbin/sysctl'

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

# config_order specifies the attribute and their order in which the wizard processes them
config_order = ('interface', 'driver', 'ssid', 'hw_mode','channel', 'macaddr_acl', 'auth_algs', 'ignore_broadcast_ssid', 'wpa', 'wpa_passphrase', 'wpa_key_mgmt', 'wpa_pairwise', 'rsn_pairwise')

# config_template specifies the attribute type, default value and available choices
# type 0 means that the attribute doesn't have any limited choices as their values
# type 1 means that the attribute value should be from one of the values specified by 'choices' list
hostapd_default = {	
		'interface' : {'type' : 0, 'default' : 'wlan0'},
		'driver' : {'type' : 0, 'default' : 'nl80211'},
		'ssid' : {'type' : 0, 'default' : 'test'},
		'hw_mode' : {'type' : 1, 'default' : 'g', 'choices' : ['a','b','g']},
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

# general defaults
general_defaults = {
	'in' : 'wlan0',
	'out' : 'eth0',
	'ip_wlan' : '10.0.0.1',
	'netmask' : '255.255.255.0',
}

# dhcpd defaults
dhcpd_defaults = {
	'ip_router' : '10.0.0.1',
	'ip_netmask' : '255.255.255.0',
	'ip_subnet' : '10.0.0.0',
	'ip_broadcast' : '10.0.0.255',
	'dns_1' : '8.8.8.8',
	'dns_2' : '8.8.4.4',
	'ip_range_min' : '10.0.0.3',
	'ip_range_max' : '10.0.0.12',
}

# dhcpd_template holds the basic layout for the /etc/py_hostapd_dhcpd.conf
# variables are enclosed within '$'s
dhcpd_template =('ddns-update-style none;\n'
'ignore client-updates;\n'
'authoritative;\n'
'option local-wpad code 252 = text;\n'
'subnet\n'
'$ip_subnet$ netmask $ip_netmask$ {\n'
'option routers\n'
'$ip_router$;\n'
'option subnet-mask\n'
'$ip_netmask$;\n'
'option broadcast-address\n'
'$ip_broadcast$;\n'
'option domain-name\n'
'"localhost";\n'
'option domain-name-servers\n'
'$ip_router$, $dns_1$, $dns_2$;\n'
'option time-offset\n'
'0;\n'
'range $ip_range_min$ $ip_range_max$;\n'
'default-lease-time 1209600;\n'
'max-lease-time 1814400;\n'
'}\n')
