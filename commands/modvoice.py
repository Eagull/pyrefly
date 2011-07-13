import xmppUtils

commandText = 'modvoice'
helpText = 'De-mods then devoices a moderator. Temporary. Admin use only.'

def process(sender, type, args, client):
	args = args.split(' ', 2)
	action = args[0]
	if action == 'off':
		if len(args) > 1:
			room = sender.getStripped()
			senderNick = sender.getResource()
			xmppUtils.setRole(room, args[1], 'participant', 'Requested by ' + senderNick)
			xmppUtils.setRole(room, args[1], 'visitor')
		
	elif action == 'on':
		if len(args) > 1:
			room = sender.getStripped()
			xmppUtils.setRole(room, args[1], 'participant')
			xmppUtils.setRole(room, args[1], 'moderator')