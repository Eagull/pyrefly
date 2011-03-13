import xmppUtils

commandText = 'voice'
helpText = 'Write arguments to the standard output.'

def process(sender, type, args, client):
	if len(args) > 0:
		room = sender.getStripped()
		senderNick = sender.getResource()
		xmppUtils.setRole(room, args, 'participant', 'Requested by ' + senderNick)
