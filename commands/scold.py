import time
import xmppUtils

commandText = 'scold'
helpText = 'Devoices a user for five, then revoices them.'


def process(sender, type, args, client):
	comSend = sender.getResource()
	room = sender.getStripped()
	if xmppUtils.isAdmin(room, comSend):
		if len(args) >0:
			naughty = '/me slaps ' + args + ' around for five seconds. NAUGHTY.'
			nice = '/me bows and returns to his alcove.'
			xmppUtils.setRole(room, args, 'visitor')
			xmppUtils.sendMessage(room, naughty , type='groupchat')
			time.sleep(5) # This is ASKING for issues.
			xmppUtils.setRole(room, args, 'participant')
			xmppUtils.sendMessage(room, nice, type='groupchat')
	elif not xmppUtils.isAdmin(room, comSend):
		xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')
