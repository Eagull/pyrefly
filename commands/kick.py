import xmppUtils

commandText = 'kick'
helpText = 'Kick the specified user.'

def process(sender, type, args, client):
	if len(args) > 0:
		room = sender.getStripped()
		senderNick = sender.getResource()
		xmppUtils.setRole(room, args, 'none', 'Requested by ' + senderNick)
		
		
