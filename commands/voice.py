import xmppUtils

commandText = 'voice'
helpText = 'Devoice the specified user.'

def process(sender, type, args, client):
	if len(args) > 0:
		room = sender.getStripped()
		senderNick = sender.getResource()
		xmppUtils.setRole(room, args, 'participant', 'Requested by ' + senderNick)
