import sys
import app_info
def exit_script():
	print '\nGoodbye!'
	sys.exit()

def display_usage():
	print app_info.name,'-', app_info.description
	print 'Version :', app_info.version
	print 'by', app_info.author
	print 'email:', app_info.email
	print 'github page:',app_info.github
	print
	print 'Usage :',
	print 'hostapd.py [action] [<options>...]'
	print
	print 'No attributes will start hostapd.py in interactive mode'
	print
	print 'Following actions are currently supported:'
	print 'start'
	print 'stop'
	print 'restart'
	print 'usage'
