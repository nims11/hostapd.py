#!/usr/bin/env python2.7
import sys
import common_methods, ConfigParser, config_hostapd
from config import bcolors
import config
global_config = {}
default_config = {}
def config_cli():
	if len(sys.argv)==3:
		if sys.argv[2] == 'list':
			keys = global_config.keys()
			for x in keys:
				print x, '=', global_config[x]
		elif global_config.has_key(sys.argv[2]):
			print sys.argv[2], '=', global_config[sys.argv[2]]
		else:
			print 'Invalid key :', sys.argv[2]
	elif len(sys.argv) == 4:
		if global_config.has_key(sys.argv[2]):
			global default_config
			sections = default_config.keys()
			for section in sections:
				length = len(default_config[section])
				for idx in range(length):
					key, val = default_config[section][idx]
					if key == sys.argv[2]:
						val = sys.argv[3]
					else:
						val = global_config[key]
					default_config[section][idx] = (key, val)
			print 'Changing \''+sys.argv[2]+'\' to \''+sys.argv[3] + '\''
			gen_default_cfg()
		else:
			print 'Invalid key :', sys.argv[2]
	else:
		common_methods.exit_error('[ERROR] config: incorrect usage', 1)
def read_default_cfg():
	global default_config
	default_config = {'HOSTAPD' : config_hostapd.get_hostapd_defaults(),
			'DHCP' : config_hostapd.get_dhcp_defaults(),
			'GENERAL' : config_hostapd.get_general_defaults(),
			'NAT' : config_hostapd.get_nat_defaults(),
			}

def gen_default_cfg():
	write_cfg(default_config['HOSTAPD'], 'HOSTAPD')
	write_cfg(default_config['DHCPD'], 'DHCPD')
	write_cfg(default_config['GENERAL'], 'GENERAL')

def write_cfg(content, section):
	configparser = ConfigParser.ConfigParser()
	try:
		with open(config.file_cfg) as f:
			configparser.read(f.name)
	except IOError as e:
		print bcolors.WARNING ,'[WARNING]', config.file_cfg, 'does not exist, new will be created', bcolors.ENDC
	try:
		configparser.add_section(section)
	except ConfigParser.DuplicateSectionError: pass

	for line in content:
		configparser.set(section, line[0],line[1])
	print 'Writing Section', section, 'to',config.file_cfg,'...' 
	try:
		with open(config.file_cfg,'wb') as f:
			configparser.write(f)
	except:
		common_methods.exit_error('[ERROR] Writing Failed!')
	print bcolors.OKGREEN, 'Done!', bcolors.ENDC

def read_cfg():
	global global_config
	global_config1 = ConfigParser.ConfigParser()
	global_config1.read(config.file_cfg)
	tup_list = global_config1.items('HOSTAPD') + global_config1.items('DHCPD') + global_config1.items('GENERAL')
	global_config = dict(i for i in tup_list)
	for sections in default_config.keys():
		for (name, value) in default_config[sections]:
			if name not in global_config:
				print name, 'not defined, using default'
				global_config[name] = value
	# print global_config, len(global_config)

def get_config():
	return global_config

def init():
	read_default_cfg()
	try:
		with open(config.file_cfg) as f: pass
	except IOError:
		print bcolors.WARNING, '[WARNING]', config.file_cfg, 'does not exist, Generating Defaults...' ,bcolors.ENDC
		gen_default_cfg()
	read_cfg()

if __name__ == '__main__':
	init()
