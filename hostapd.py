#!/usr/bin/env python2.7
import sys
from HPS import start_hostapd, stop_hostapd, restart_hostapd
from config_hostapd import config_hostapd_default, config_non_interactive
from functools import partial
from common_methods import exit_script, display_usage

def interactive():
	"""
	Starts Interactive Session
	"""
	print 'Interactive Session'
	print '1= Start Hostapd; ',
	print '2= Stop Hostapd; ',
	print '3= Restart Hostapd; ',
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
	"""
	The starting base
	"""
	# Check for py_hostapd.conf
	try:
		with open('/etc/py_hostapd.conf') as f: pass
	except IOError as e:
		print "[ERROR] /etc/py_hostapd.conf Not Found, Generating Default!"
		config_hostapd_default()

	# Start interactive() if no arguments
	if len(sys.argv) == 1:
			interactive()
	else:
		actions = { 'start' : start_hostapd,
				'stop' : stop_hostapd,
				'restart' : restart_hostapd,
				'config' : config_non_interactive,
				'help' : display_usage,
				'-h' : display_usage,
				}

		if sys.argv[1] in actions:
			actions[sys.argv[1]]()
		else:
			print '[ERROR] Invalid Argument\n'
			display_usage()
	exit_script()

if __name__ == '__main__':
	main()
