import xmppUtils

commandText = 'say'
helpText = 'Write arguments to the standard output.'

def process(sender, type, args, client):
	if len(args) > 0:
		room = sender.getStripped()
		xmppUtils.sendMessage(room, args, type='groupchat')