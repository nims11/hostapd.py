#!/usr/bin/env python2.7
from common_methods import exit_script, display_usage, exit_error
import sys
from config import config_template, config_order, general_defaults
def get_general_defaults():
	content = []
	for key in general_defaults.keys():
		content.append((key,general_defaults[key]))
	return content

def config_hostapd_default(ret = False):
	"""
	Config using the default values for the attributes
	"""
	config = []
	for attribute in config_order:
		value = config_template[attribute]
		foo = config_template[attribute]['default']
		config.append((attribute, foo))
	if ret:
		return config
	print 'Writing Default /etc/py_hostapd.conf...'
	write_hostapd_conf(config)

def config_hostapd():
	"""
	Config Wizard
	"""

	# Holds the final config data [ (attrib, value),....]
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
	if len(sys.argv) == 3:
		if sys.argv[2] == 'wizard':
			config_hostapd()
		elif sys.argv[2] == 'defaults':
			config_hostapd_default()
		else:
			exit_error('[ERROR] Missing/Too Many arguments', 1)
	elif len(sys.argv) != 4:
		exit_error('[ERROR] Missing/Too Many arguments', 1)
	else:
		if sys.argv[2] == 'password' or sys.argv[2] == 'key':
			change_attr('wpa_passphrase',sys.argv[3])
		else:
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
