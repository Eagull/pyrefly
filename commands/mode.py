import xmppUtils

commandText = 'mode'
helpText = 'Sets the affiliation of a user. For admin use.'

def process(sender, type, args, client):
	room = sender.getStripped()
	args = args.split(' ', 2)
	if len(args) < 2:
		if len(args) == 1:
			return checkmode(args[0],room)
		else:
			return 0
	action = args[0]
	who = args[1]
	if action == 'check': checkmode(who,room)
	memGrant = '%s: Membership granted!' %(args[1])
	memRevoke = '%s: Membership revoked!' %(args[1])
	modGrant = '%s: Moderator permissions granted!' %(args[1])
	modRevoke = '%s: Moderator permissions revoked!' %(args[1])
	comSend = sender.getResource()

	if action == '+m':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setAffiliation(room, who, 'member')
				xmppUtils.sendMessage(room, memGrant, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '+M':
		#works
		if xmppUtils.isAdmin(room, comSend):
			xmppUtils.setRole(room, who, 'moderator')
			xmppUtils.sendMessage(room, modGrant, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '+A':
		#TODO# Make work
		if xmppUtils.isOwner(room, comSend):
			xmppUtils.setAffiliation(room, who, 'administrator')

	elif action == '-m':
		#works
		if xmppUtils.isMod(room, comSend):
			if len(args) > 1:
				xmppUtils.setAffiliation(room, who, 'none')
				xmppUtils.sendMessage(room, memRevoke, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '-M':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setRole(room, who, 'participant')
				xmppUtils.sendMessage(room, modRevoke, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '-A':
		#TODO# Make work
		if xmppUtils.isAdmin(room, comSend):
			xmppUtils.setAffiliation(room, who, 'member')

	elif action == 'help':
		if '+m' in args:
			xmppUtils.sendMessage(room, 'Admin: grants membership.', type='groupchat')
		elif '-m' in args:
			xmppUtils.sendMessage(room, 'Admin: revokes membership.', type='groupchat')
		elif '+M' in args:
			xmppUtils.sendMessage(room, 'Admin: grants moderator access.', type='groupchat')
		elif '-M' in args:
			xmppUtils.sendMessage(room, 'Admin: revokes moderator access.', type='groupchat')
		elif '+A' in args:
			xmppUtils.sendMessage(room, 'To be implemented: sets administrator privileges.', type='groupchat')
		elif '-A' in args:
			xmppUtils.sendMessage(room, 'To be implemented: revokes administrator privileges.', type='groupchat')


def checkmode(who, room):
	if len(who) < 1: return -1
	if xmppUtils.isAdmin(room, who):
		xmppUtils.sendMessage(room, 'Administrator', type='groupchat')
	elif xmppUtils.isModerator(room, who):
		xmppUtils.sendMessage(room, 'Moderator', type='groupchat')
	elif xmppUtils.isMember(room, who):
		xmppUtils.sendMessage(room, 'Member', type='groupchat')
	return 0

