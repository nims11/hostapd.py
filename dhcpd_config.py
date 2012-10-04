from common_methods import exit_script
from config import network_settings, dhcpd_template
import sys

def gen_dhcpd():
	content = dhcpd_template[:]
	for key in network_settings.keys():
		if key[0]=='$' and key[len(key)-1]=='$':
			content = content.replace(key, network_settings[key])
	write_dhcpd(content)

def write_dhcpd(content):
	try:
		with open('/etc/py_dhcpd.conf', 'w') as f:
			f.write( content )
	except:
		exit_error('[ERROR] Failed to open /etc/py_dhcpd.conf')


