#!/usr/bin/env python2.7
import subprocess;
from time import sleep
IN = 'wlan0'
OUT = 'eth0'
IP = '10.0.0.1'
def start_hostapd():
	"""
	Starts Hostapd
	"""
	print
	try:
		with open('/etc/py_hostapd.conf') as f: pass
	except IOError as e:
		print 'No config file exists!' # do you want to create one?
	print 'configuring',IN,'...'
	setup_wlan = subprocess.Popen(['ifconfig', IN, 'up', IP, 'netmask', '255.255.255.0'])
	sleep(1)
	dhcp_log = open('./dhcp.log', 'w')
	print 'Starting dhcpd...'
	dhcp_proc = subprocess.Popen(['dhcpd',IN],stdout = dhcp_log, stderr = dhcp_log) 
	sleep(1)
	dhcp_log.close();
	print 'Configuring iptables...'
	subprocess.call(['iptables','--flush'])
	subprocess.call(['iptables','--table','nat','--flush'])
	subprocess.call(['iptables','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--append','POSTROUTING','--out-interface',OUT,'-j','MASQUERADE'])
	subprocess.call(['iptables','--append','FORWARD','--in-interface',IN,'-j','ACCEPT'])
	subprocess.call(['sysctl','-w','net.ipv4.ip_forward=1'])
	
	print 'Starting Hostapd...'
	hostapd_proc = subprocess.Popen(['hostapd -t -d /etc/py_hostapd.conf >./hostapd.log'],shell=True)
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
