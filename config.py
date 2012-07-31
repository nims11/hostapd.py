#!/usr/bin/env python2.7
config_template = {	
		'interface' : {'type' : 0, 'default' : 'wlan0'},
		'driver' : {'type' : 0, 'default' : 'nl80211'},
		'ssid' : {'type' : 0, 'default' : 'test'},
		'hw_mode' : {'type' : 1, 'default' : 'g', 'choices' : ['a','b','g','n']},
		'channel' : {'type' : 1, 'default' : '6', 'choices' : [x for x in range(1,12)]},
		'macaddr_acl' : {'type' : 1, 'default' : 0, 'choices' : [0,1,2]},
		'auth_algs' : {'type' : 1, 'default' : 1, 'choices' : [1,2,3]},
		'ignore_broadcast_ssid' : {'type' : 1, 'default' : 0, 'choices' : [0,1,2]},
		'wpa' : {'type' : 1, 'default' : 3, 'choices' : [1,2,3]},
		'wpa_passphrase' : {'type' : 0, 'default' : 'foobar123'},
		'wpa_key_mgmt' : {'type' : 1, 'default' : 'WPA-PSK', 'choices' : ['WPA-PSK','WPA-EAP','WPA-PSK WPA-EAP']},
		'wpa_pairwise' : {'type' : 1, 'default' : 'TKIP', 'choices' : ['TKIP','CCMP']},
		'rsn_pairwise' : {'type' : 1, 'default' : 'CCMP', 'choices' : ['TKIP','CCMP']},
		}
def config_hostapd():
	pass
