import xmppUtils

commandText = 'devoice'
helpText = 'Devoice the specified user.'

def process(sender, type, args, client):
	room = sender.getStripped()
	comSend = sender.getResource()
	if xmppUtils.isModerator(room, comSend):
		if len(args) > 0:
			senderNick = sender.getResource()
			xmppUtils.setRole(room, args, 'visitor', 'Requested by ' + senderNick)
	elif not xmppUtils.isAdmin(room, comSend):
		xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')
