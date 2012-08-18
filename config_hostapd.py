#!/usr/bin/env python2.7
from common_methods import exit_script, display_usage, exit_error
import sys

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
		'ieee80211n' : {'type' : 1, 'default' : 0, 'choices' : ['0','1']},
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
def config_hostapd_default():
	"""
	Config using the default values for the attributes
	"""
	config = []
	for attribute in config_order:
		value = config_template[attribute]
		foo = config_template[attribute]['default']
		config.append((attribute, foo))
	print 'Writing Default /etc/py_hostapd.conf...'
	write_hostapd_conf(config)

def config_hostapd():
	"""
	Config Wizard
	"""
	config = []
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
			try:
				foo = raw_input()
			except KeyboardInterrupt:
				exit_script()
			if len(foo) == 0:
				foo = config_template[attribute]['default']
			config.append((attribute,foo))
		elif config_template[attribute]['type'] == 1:
			while True:
				try:
					foo = raw_input()
				except KeyboardInterrupt:
					exit_script()
				if len(foo) == 0:
					foo = config_template[attribute]['default']
				if foo in config_template[attribute]['choices']:
					config.append((attribute, foo))
					break;
				else:
					print 'Invalid Input\n:',
	write_hostapd_conf(config)

def write_hostapd_conf(config):
	"""
	Writes the config data to /etc/py_hostapd.conf
	"""
	print '\nConfirm Write? [y/N] ? ',
	ch = raw_input()
	if ch == 'y' or ch == 'Y':
		try:
			with open('/etc/py_hostapd.conf', 'w') as f:
				for attr in config:
					f.write( str(attr[0]) + '=' + str(attr[1]) + '\n' )
		except:
			exit_error('[ERROR] Failed to open /etc/py_hostapd.conf')

def config_non_interactive():
	if len(sys.argv) < 4:
		exit_error('[ERROR] Missing arguments', 1)
	change_attr(sys.argv[2],sys.argv[3])

def change_attr_interactive(attr):
	print '\nEnter New',attr,': ',
	while True:
		try:
			new_attr = raw_input()
		except KeyboardInterrupt:
			exit_script()
		if len(new_attr) !=0:
			break;
	change_attr(attr,new_attr)

def change_attr(attr,new_attr):
	"""
	Changes the 'attr' attribute in /etc/py_hostapd.conf
	"""
	if attr not in config_template:
		exit_error('[ERROR] Invalid attribute \'',attr,'\'', 1)
	if config_template[attr]['type'] == 1 and new_attr not in config_template[attr]['choices']:
		exit_error('[ERROR] Invalid attribute value \'',new_attr,'\'',1)

	new_content = ""
	try:
		with open('/etc/py_hostapd.conf','r+') as f:
			for line in f:
				if line.find(attr) != 0:
					new_content += line
				else:
					new_content += attr + '=' + new_attr + "\n"
			f.seek(0)
	except:
		exit_error('[ERROR] Failed to open /etc/py_hostapd.conf')
	try:
		with open('/etc/py_hostapd.conf','w') as f:
			f.write(new_content)
	except:
		exit_error('[ERROR] Failed to open /etc/py_hostapd.conf')

if __name__ == '__main__':
	config_hostapd()
