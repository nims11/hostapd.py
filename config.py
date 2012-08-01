#!/usr/bin/env python2.7
config_order = ('interface', 'driver', 'ssid', 'hw_mode', 'channel', 'macaddr_acl', 'auth_algs', 'ignore_broadcast_ssid', 'wpa', 'wpa_passphrase', 'wpa_key_mgmt', 'wpa_pairwise', 'rsn_pairwise')
config_template = {	
		'interface' : {'type' : 0, 'default' : 'wlan0'},
		'driver' : {'type' : 0, 'default' : 'nl80211'},
		'ssid' : {'type' : 0, 'default' : 'test'},
		'hw_mode' : {'type' : 1, 'default' : 'g', 'choices' : ['a','b','g','n']},
		'channel' : {'type' : 1, 'default' : '6', 'choices' : [str(x) for x in range(1,12)]},
		'macaddr_acl' : {'type' : 1, 'default' : 0, 'choices' : [0,1,2]},
		'auth_algs' : {'type' : 1, 'default' : 1, 'choices' : [1,2,3]},
		'ignore_broadcast_ssid' : {'type' : 1, 'default' : 0, 'choices' : [0,1,2]},
		'wpa' : {'type' : 1, 'default' : 3, 'choices' : [1,2,3]},
		'wpa_passphrase' : {'type' : 0, 'default' : 'foobar123'},
		'wpa_key_mgmt' : {'type' : 1, 'default' : 'WPA-PSK', 'choices' : ['WPA-PSK','WPA-EAP','WPA-PSK WPA-EAP']},
		'wpa_pairwise' : {'type' : 1, 'default' : 'TKIP', 'choices' : ['TKIP','CCMP']},
		'rsn_pairwise' : {'type' : 1, 'default' : 'CCMP', 'choices' : ['TKIP','CCMP']},
		}
config = []
def config_hostapd():
	"""
	Config Wizard
	"""
	print 'Hostapd Config Wizard...\n'
	for attribute in config_order:
		value = config_template[attribute]
		print attribute, ':',
		if config_template[attribute]['type'] == 1:
			print '[',
			for choice in config_template[attribute]['choices']:
				print choice,'/',
			print '\b\b]',
		print '[ default =', config_template[attribute]['default'],']\n',':',
		
		if config_template[attribute]['type'] == 0:
			foo = raw_input()
			if len(foo) == 0:
				foo = config_template[attribute]['default']
			config.append((attribute,foo))
		elif config_template[attribute]['type'] == 1:
			while True:
				foo = raw_input()
				if len(foo) == 0:
					foo = config_template[attribute]['default']
				if foo in config_template[attribute]['choices']:
					config.append((attribute, foo))
					break;
				else:
					print 'Invalid Input\n:',
	print config

