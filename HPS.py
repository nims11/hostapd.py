#!/usr/bin/env python2.7
import subprocess
from time import sleep
import config
from common_methods import exit_script
import sys
import config_gen

def start_hostapd():
	"""
	Configs the IN interface, starts dhcpd, configs iptables, Starts Hostapd
	"""
	global_config = config_gen.get_config()
	IN = global_config['in']
	OUT = global_config['out']
	IP = global_config['ip_wlan']
	NETMASK = global_config['netmask']
	try:
		with open(config.file_hostapd) as f: pass
	except IOError as e:
		exit_error('[ERROR] ' + config.file_hostapd + ' doesn\'t exist')
	
	# Configure network interface
	print 'configuring',IN,'...'
	setup_wlan = subprocess.Popen(['ifconfig', IN, 'up', IP, 'netmask', NETMASK])
	sleep(1)
	dhcp_log = open('./dhcp.log', 'w')

	# Start dhcpd
	print 'Starting dhcpd...'
	dhcp_proc = subprocess.Popen(['dhcpd',IN, '-cf', config.file_dhcpd],stdout = dhcp_log, stderr = dhcp_log) 
	sleep(1)
	dhcp_log.close();

	# Configure iptables
	print 'Configuring iptables...'
	subprocess.call(['iptables','--flush'])
	subprocess.call(['iptables','--table','nat','--flush'])
	subprocess.call(['iptables','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--append','POSTROUTING','--out-interface',OUT,'-j','MASQUERADE'])
	subprocess.call(['iptables','--append','FORWARD','--in-interface',IN,'-j','ACCEPT'])
	subprocess.call(['sysctl','-w','net.ipv4.ip_forward=1'])
	
	# Start hostapd
	print 'Starting Hostapd...'
	hostapd_proc = subprocess.Popen(['hostapd -t -d '+config.file_hostapd+' >./hostapd.log'],shell=True)
	print 'Done... (Hopefully!)'
	print

def stop_hostapd():
	"""
	Stops Hostapd and dhcpd
	"""
	print
	print 'Killing Hostapd...'
	subprocess.call(['killall','hostapd'])
	print 'Killing dhcpd...'
	subprocess.call(['killall','dhcpd'])
	print

def restart_hostapd():
	stop_hostapd()
	# Workaround for issues with dhcpd
	sleep(2)

	start_hostapd()
