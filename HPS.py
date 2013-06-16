#!/usr/bin/env python2.7
import subprocess
from time import sleep
import config
from common_methods import exit_script, exit_error
import sys
import config_gen
from config_hostapd import generate_confs
import shlex
import os

def start_hostapd():
	"""
	Configs the IN interface, starts dhcpd, configs iptables, Starts Hostapd
	"""
	generate_confs()
	conf = config_gen.get_config()
	env_tups = [(section+'_'+key, val) for section in conf.keys() for key, val in conf[section].items()]
	env_dict = dict(os.environ.items() + env_tups)
	
	print 'Starting...'
	for section in config.script_order:
		print 'Executing %s for [%s]...' % (conf[section]['SCRIPT'], section),
		ret = subprocess.call(conf[section]['SCRIPT'], env=env_dict)
		if ret == 0:
			print 'Done!'
		else:
			print 'Failed!'
			exit_error('[ERROR] Failed to initiate [%s], check log file %s' % (section, conf[section]['LOGFILE']))
		


def stop_hostapd():
	"""
	Stops Hostapd and dhcpd
	"""
	conf = config_gen.get_config()
	env_tups = [(section+'_'+key, val) for section in conf.keys() for key, val in conf[section].items()]
	env_dict = dict(os.environ.items() + env_tups)

	print 'Stopping...'
	for section in config.script_order[::-1]:
		if conf[section].has_key('EXIT_SCRIPT'):
			print 'Executing %s for [%s]...' % (conf[section]['EXIT_SCRIPT'], section)
			ret = subprocess.call(conf[section]['EXIT_SCRIPT'], env=env_dict)
			if ret == 0:
				print 'Done!'
			else:
				print 'Failed!'
				exit_error('[ERROR] Failed to exit [%s], check log file %s' % (section, conf[section]['LOGFILE']))
#	print
#	print 'Killing Hostapd...'
#	subprocess.call(['killall','hostapd'])
#	print 'Killing dhcpd...'
#	subprocess.call(['killall','dhcpd'])
#	print

def restart_hostapd():
	stop_hostapd()

	# Workaround for issues with dhcpd
	sleep(2)

	start_hostapd()
