#!/usr/bin/env python2.7
import sys
from HPS import start_hostapd, stop_hostapd, restart_hostapd
from config_hostapd import config_hostapd, config_hostapd_default, change_attr, change_attr_interactive, config_non_interactive
from functools import partial
from common_methods import exit_script, display_usage

def config_interactive():
	"""
	Interactive Config mode
	"""
	print '\nConfigure...\n'
	print '1= Configure hostapd.conf; ',
	print '2= Change ssid;',
	print '3= Change WPA passphrase;',
	print '0= exit'
	while True:
		try:
			print 'Enter Choice : ',
			ch = int(raw_input())
			break;
		except KeyboardInterrupt:
			exit_script()
		except:
			continue;

	options = { 0 : exit_script,
			1 : config_hostapd,
			#2 : config_dhcpd,
			2 : partial(change_attr_interactive,'ssid'),
			3 : partial(change_attr_interactive,'wpa_passphrase'),
			}
	while ch not in options:
		print 'Invalid Option'
		try:
			print 'Enter Choice : ',
			ch = int(raw_input())
		except KeyboardInterrupt:
			exit_script()
		except:
			continue;
	options[ch]();


def interactive():
	"""
	Starts Interactive Session
	"""
	print 'Interactive Session'
	print '1= Start Hostapd; ',
	print '2= Stop Hostapd; ',
	print '3= Restart Hostapd; ',
	print '4= Configure; ',
	print '0= exit'
	while True:
		try:
			print 'Enter Choice : ',
			ch = int(raw_input())
			break;
		except KeyboardInterrupt:
			exit_script()
		except:
			continue;

	options = { 0 : exit_script,
			1 : start_hostapd,
			2 : stop_hostapd,
			3 : restart_hostapd,
			4 : config_interactive,
			}
	while ch not in options:
		print 'Invalid Option'
		try:
			print 'Enter Choice : ',
			ch = int(raw_input())
		except KeyboardInterrupt:
			exit_script()
		except:
			continue
	
	options[ch]()


def main():
	try:
		with open('/etc/py_hostapd.conf') as f: pass
	except IOError as e:
		print "[ERROR] /etc/py_hostapd.conf Not Found!"
		config_hostapd_default()
	if len(sys.argv) == 1:
		while True:
			interactive()
	actions = { 'start' : start_hostapd,
			'stop' : stop_hostapd,
			'restart' : restart_hostapd,
			'usage' : display_usage,
			'config' : config_non_interactive,
			}

	if sys.argv[1] in actions:
		actions[sys.argv[1]]()
	else:
		print '[ERROR] Invalid Argument\n'
		display_usage()

if __name__ == '__main__':
	main()
