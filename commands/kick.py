import xmppUtils

commandText = 'kick'
helpText = 'Kick the specified user.'

def process(sender, type, args, client):
	comSend = sender.getResource()
	room = sender.getStripped()
	if xmppUtils.isModerator(room, comSend):
		if len(args) > 0:
			senderNick = sender.getResource()
			xmppUtils.setRole(room, args, 'none', '...cause the kickin\' boot has granted its powers to %s' %(comSend))