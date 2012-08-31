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

network_settings = {
		'IN' : 'wlan0',
		'OUT' : 'eth0',
		'IP' : '10.0.0.1',
		'NETMASK' : '255.255.255.0',
		}
