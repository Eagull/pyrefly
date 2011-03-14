from subprocess import Popen, PIPE
import xmppUtils

commandText = 'date'
helpText = 'Print the current date and time.'

def process(sender, type, args, client):
	response = Popen(["date"], stdout=PIPE).communicate()[0].split('\n')[0]
	xmppUtils.sendMessage(sender, response, type)