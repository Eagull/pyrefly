import xmppUtils

commandText = 'shout'
helpText = 'Say something to all rooms.'

def process(sender, type, args, client):
#	if sender.isAdmin:
	if len(args) > 0:
#		if sender.isAdmin:
		orgin = sender.getStripped()
		print orgin
		for room in xmppUtils.rosters:
			#~ print room
			xmppUtils.sendMessage(room, args, type='groupchat')
#		else:
#			xmppUtils.sendMessage(room, 'Sorry, unauthorized.', type='chat')
