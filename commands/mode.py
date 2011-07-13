import xmppUtils

commandText = 'mode'
helpText = 'Sets the affiliation of a user. For admin use.'

def process(sender, type, args, client):
	args = args.split(' ', 2)
	if len(args) < 2: return 0
	action = args[0]
	room = sender.getStripped()
	memGrant = '%s: Membership granted!' %(args[1])
	memRevoke = '%s: Membership revoked!' %(args[1])
	modGrant = '%s: Moderator permissions granted!' %(args[1])
	modRevoke = '%s: Moderator permissions revoked!' %(args[1])
	comSend = sender.getResource()
	if action == '+m':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setAffiliation(room, args[1], 'member')
				xmppUtils.sendMessage(room, memGrant, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '+M':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setRole(room, args[1], 'moderator')
				xmppUtils.sendMessage(room, modGrant, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '+A':
		#TODO# Make work
		if len(args) > 1:
			xmppUtils.setAffiliation(room, args[1], 'administrator')

	elif action == '-m':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setAffiliation(room, args[1], 'none')
				xmppUtils.sendMessage(room, memRevoke, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '-M':
		#works
		if xmppUtils.isAdmin(room, comSend):
			if len(args) > 1:
				xmppUtils.setRole(room, args[1], 'participant')
				xmppUtils.sendMessage(room, modRevoke, type='groupchat')
		elif not xmppUtils.isAdmin(room, comSend):
			xmppUtils.sendMessage(room, 'Unauthorized.', type='groupchat')

	elif action == '-A':
		#TODO# Make work
		if len(args) > 1:
			xmppUtils.setAffiliation(room, args[1], 'member')

	elif action == 'help':
		if len(args) > 1 and '+m' in args:
			xmppUtils.sendMessage(room, 'Admin: grants membership.', type='groupchat')
		elif len(args) > 1 and '-m' in args:
			xmppUtils.sendMessage(room, 'Admin: revokes membership.', type='groupchat')
		elif len(args) > 1 and '+M' in args:
			xmppUtils.sendMessage(room, 'Admin: grants moderator access.', type='groupchat')
		elif len(args) > 1 and '-M' in args:
			xmppUtils.sendMessage(room, 'Admin: revokes moderator access.', type='groupchat')
		elif len(args) > 1 and '+A' in args:
			xmppUtils.sendMessage(room, 'To be implemented: sets administrator privileges.', type='groupchat')
		elif len(args) > 1 and '-A' in args:
			xmppUtils.sendMessage(room, 'To be implemented: revokes administrator privileges.', type='groupchat')

	elif action == 'check':
		if len(args[1]) > 1:
			if xmppUtils.isAdmin(room, args[1]):
				xmppUtils.sendMessage(room, 'Administrator', type='groupchat')
		elif len(args[1]) > 1:
			if xmppUtils.isModerator(room, args[1]):
				xmppUtils.sendMessage(room, 'Moderator', type='groupchat')
		elif len(args[1]) > 1:
			if xmppUtils.isMember(room, args[1]):
				xmppUtils.sendMessage(room, 'Member', type='groupchat')

