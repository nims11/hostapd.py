#!/usr/bin/env python2.7
import sys
import common_methods, ConfigParser, config_hostapd
from common_methods import exit_error
from config import bcolors
import config
global_config = {}
default_config = {}
def config_cli():

	# ./hostapd.py config
	if len(sys.argv) == 2:
		for section in global_config.keys():
			print '[%s]' % section
			for key, val in global_config[section].items():
				print '%s = %s' %(key,val)
			print
	
	# ./hostapd.py config <section>
	elif len(sys.argv) == 3:
		section = sys.argv[2]
		if global_config.has_key(section):
			print '[%s]' % section
			for key, val in global_config[section].items():
				print '%s = %s' % (key, val)
		else:
			exit_error('[%s] Does not exist' % section)
	
	# ./hostapd.py config <section> <key>
	elif len(sys.argv) == 4:
		section = sys.argv[2]
		key = sys.argv[3]
		if global_config.has_key(section):
			if global_config[section].has_key(key):
				print global_config[section][key]
			else:
				exit_error('No key %s in [%s]' % (key, section))
		else:
			exit_error('[%s] Does not exist' % section)
	
	# ./hostapd.py config <section> <key> <val>
	elif len(sys.argv) == 5:
		section = sys.argv[2]
		key = sys.argv[3]
		val = sys.argv[4]
		import copy
		conf = copy.deepcopy(global_config)
		conf[section][key] = val
		gen_default_cfg(conf)

def read_default_cfg():
	"""
	Write to default_config
	"""
	global default_config
	default_config = {
			'HOSTAPD' : config_hostapd.get_hostapd_defaults(),
			'DHCP' : config_hostapd.get_dhcp_defaults(),
			'GENERAL' : config_hostapd.get_general_defaults(),
			'NAT' : config_hostapd.get_nat_defaults(),
			}
	for section in default_config.keys():
		default_config[section] = dict(default_config[section])

def gen_default_cfg(config):
	write_cfg(config['HOSTAPD'], 'HOSTAPD')
	write_cfg(config['DHCP'], 'DHCP')
	write_cfg(config['GENERAL'], 'GENERAL')
	write_cfg(config['NAT'], 'NAT')

def write_cfg(content, section):
	configparser = ConfigParser.ConfigParser()
	configparser.optionxform = str
	try:
		with open(config.file_cfg) as f:
			configparser.read(f.name)
	except IOError as e:
		print bcolors.WARNING ,'[WARNING]', config.file_cfg, 'does not exist, new will be created', bcolors.ENDC
	try:
		configparser.add_section(section)
	except ConfigParser.DuplicateSectionError: pass

	for key, val in content.items():
		configparser.set(section, key, val)
	print 'Writing Section', section, 'to',config.file_cfg,'...' 
	try:
		with open(config.file_cfg,'wb') as f:
			configparser.write(f)
	except:
		common_methods.exit_error('[ERROR] Writing Failed!')
	print bcolors.OKGREEN, 'Done!', bcolors.ENDC

def read_cfg():
	"""
	Initially copies the default_config to global_config and then overwrite values found from config file
	"""
	import copy
	global global_config
	config_parse = ConfigParser.ConfigParser()
	config_parse.optionxform = str
	config_parse.read(config.file_cfg)
	global_config = copy.deepcopy(default_config)
	for section in config_parse.sections():
		for (name, value) in config_parse.items(section):
			global_config[section][name] = value

def get_config():
	return global_config

def init():
	"""
	If config file exists, reads it, else generates a default one
	"""
	read_default_cfg()
	try:
		with open(config.file_cfg) as f: pass
	except IOError:
		print bcolors.WARNING, '[WARNING]', config.file_cfg, 'does not exist, Generating Defaults...' ,bcolors.ENDC
		gen_default_cfg(default_config)
	read_cfg()

if __name__ == '__main__':
	init()
