from common_methods import exit_script
import sys

# dhcpd_template holds the basic layout for the /etc/py_hostapd_dhcpd.conf
# variables are enclosed within '$'s
dhcpd_template ='ddns-update-style none;'
'ignore client-updates;'
'authoritative;'
'option local-wpad code 252 = text;'
'subnet'
'$IP_subnet$ netmask $NETMASK$ {'
'option routers'
'$IP_router$;'
'option subnet-mask'
'$NETMASK$;'
'option broadcast-address'
'$IP_broadcast$;'
'option domain-name'
'"localhost";'
'option domain-name-servers'
'$IP_router$, 8.8.8.8, 8.8.4.4;'
'option time-offset'
'0;'
'range $IP_range_min$ $IP_range_max$;'
'default-lease-time 1209600;'
'max-lease-time 1814400;'
'}'

