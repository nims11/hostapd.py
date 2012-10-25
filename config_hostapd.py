#!/usr/bin/env python2.7
from common_methods import exit_script, display_usage, exit_error
import sys
import config
import config_gen
def generate_confs():
	write_hostapd_conf()
	write_dhcpd_conf()

def write_dhcpd_conf():
	print 'Writing /etc/py_dhcpd.conf...'
	global_config = config_gen.get_config()
	content = config.dhcpd_template[:]
	for key in config.dhcpd_defaults.keys():
		key2 = '$' + key + '$'
		content = content.replace(key2, global_config[key])
	try:
		with open('/etc/py_dhcpd.conf', 'w') as f:
			f.write( content )
	except:
		exit_error('[ERROR] Failed to open /etc/py_dhcpd.conf')


def get_general_defaults():
	"""
	Get Default General config
	"""
	content = []
	for key in config.general_defaults.keys():
		content.append((key,config.general_defaults[key]))
	return content

def get_dhcpd_defaults():
	content = []
	for key in config.dhcpd_defaults.keys():
		content.append((key,config.dhcpd_defaults[key]))
	return content

def get_hostapd_default():
	"""
	Get Default hostapd config
	"""
	ret = []
	for attribute in config.config_order:
		value = config.hostapd_default[attribute]
		foo = config.hostapd_default[attribute]['default']
		ret.append((attribute, foo))
	return ret

def write_hostapd_conf():
	"""
	Writes the config data to /etc/py_hostapd.conf
	"""
	print 'Writing /etc/py_hostapd.conf...'
	global_config = config_gen.get_config()
	try:
		with open('/etc/py_hostapd.conf', 'w') as f:
			for attr in config.hostapd_default:
				f.write( attr + '=' + global_config[attr] + '\n' )
	except:
		exit_error('[ERROR] Failed to open /etc/py_hostapd.conf')
def test():
	config_gen.init()
	generate_confs()

if __name__ == '__main__':
	test()
