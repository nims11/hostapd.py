#!/usr/bin/env python2.7
import sys
from HPS import start_hostapd, stop_hostapd
from config_hostapd import config_hostapd, change_attr
from functools import partial
#from config_dhcpd import config_dhcpd

def exit_script():
	print '\nGoodbye!'
	sys.exit()
def interactive():
	"""
	Starts Interactive Session
	"""
	print 'Interactive Session'
	print '1= Start Hostapd; ',
	print '2= Stop Hostapd; ',
	print '3= Configure hostapd.conf; ',
	print '4= Configure dhcpd.conf; ',
	print '5= Change ssid;',
	print '6= Change WPA passphrase;',
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
			3 : config_hostapd,
			#4 : config_dhcpd,
			5 : partial(change_attr,'ssid'),
			6 : partial(change_attr,'wpa_passphrase'),
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


def main():
	if len(sys.argv) == 1:
		while True:
			interactive()

if __name__ == '__main__':
	main()
