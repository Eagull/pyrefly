import xmppUtils

commandText = 'selfcheck'
helpText = 'Just looking to see if this works...'

def process(sender, type, args, client):
	room = sender.getStripped()
	me = sender.getResource()
	if len(args) == 0 and xmppUtils.isOwner(room, me):
		xmppUtils.sendMessage(room, 'This is Skullz checking this...', type='groupchat')
	elif len(args) == 0 and xmppUtils.isMember(room, me):
		xmppUtils.sendMessage(room, 'This is still probably Skullz checking this.', type='groupchat')