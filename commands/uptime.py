from subprocess import Popen, PIPE
import xmppUtils

commandText = 'uptime'
helpText = 'Tell how long the system has been running.'

def process(sender, type, args, client):
	try:
		response = Popen(["uptime"], stdout=PIPE).communicate()[0].split('\n')[0]
	except WindowsError: # Bloody windows...
		return 0
	xmppUtils.sendMessage(sender, response, type)