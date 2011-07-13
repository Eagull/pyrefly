#~ from subprocess import Popen, PIPE
import xmppUtils
import datetime

commandText = 'date'
helpText = 'Print the current date and time.'

def process(sender, type, args, client):
	# TODO: Implament timezones.
	#~ time = Popen(["date"], stdout=PIPE).communicate()[0].split('\n')[0] # No idea what the hell THAT is
	time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
	xmppUtils.sendMessage(sender, time, type)