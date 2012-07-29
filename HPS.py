#!/usr/bin/env python2.7
import subprocess;
IN = 'wlan0'
OUT = 'eth0'
IP = '10.0.0.1'
def start_hostapd():
	"""
	Starts Hostapd
	"""
	try:
		with open('hostapd.conf') as f: pass
	except IOError as e:
		print 'No config file exists!' # do you want to create one?
	setup_wlan = subprocess.Popen(['ifconfig', IN, 'up', IP, 'netmask', '255.255.255.0'])
	dhcp_log = open('./dhcp.log', 'w')
	dhcp_err_log = open('./dhcp_error.log', 'w')
	dhcp_proc = subprocess.Popen(['dhcpd',IN],stdout = dhcp_log, stderr = dhcp_err_log) 
	subprocess.call(['iptables','--flush'])
	subprocess.call(['iptables','--table','nat','--flush'])
	subprocess.call(['iptables','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--append','POSTROUTING','--out-interface',OUT,'-j','MASQUERADE'])
	subprocess.call(['iptables','--append','FORWARD','--in-interface',IN,'-j','ACCEPT'])
	subprocess.call(['sysctl','-w','net.ipv4.ip_forward=1'])

	hostapd_log = open('./hostapd.log', 'w')
	hostapd_err_log = open('./hostapd_error.log', 'w')

	hostapd_proc = subprocess.Popen(['hostapd','hostapd.conf'],stdout = hostapd_log, stderr = hostapd_err_log)

def stop_hostapd():
	"""
	Stops Hostapd and dhcpd
	"""
	subprocess.call(['killall','hostapd'])
	subprocess.call(['killall','dhcpd'])
