from omegleXmpp import OmegleClient
from random import choice
import config
import xmppUtils

commandText = 'omegle'
helpText = 'Fetch a random stranger from omegle.'
contexts = ['groupchat', 'private']

# TODO: cap the number of sessions
# TODO: check for valid nicknames

nickList = eval(config.get("nickList", "omegle"))

omegleSessions = {}

def getNick(maxTries=5):
	if not maxTries:
		maxTries = 5
	tries = 0
	nick = None
	while tries < maxTries:
		nick = choice(nickList)
		if not nick in omegleSessions:
			return nick
		tries = tries + 1

def process(sender, type, args, client):
	if not args:
		args = 'help'

	args = args.split(' ', 2)

	action = args[0]
	if len(args) > 1:
			nick = args[1]
	else:
		nick = None

	if nick in omegleSessions and not omegleSessions[nick].connected:
		del omegleSessions[nick]

	if action == 'start':
		if nick:
			if nick in omegleSessions:
				xmppUtils.sendMessage(sender, '.' + sender.getResource() + ": already present: " + nick, type)
				return
		else:
			nick = getNick(nick)
			if not nick:
				xmppUtils.sendMessage(sender, '.' + sender.getResource() + ": failed to find a random nick", type)
				return

		omegle = OmegleClient(sender.getStripped(), nick)
		omegleSessions[nick] = omegle
		omegle.start()
#		xmppUtils.sendMessage(sender, sender.getResource() + ": added - " + nick, type)

	elif action == 'stop' or action == 'off':
		if len(omegleSessions) == 0:
			return

		if nick:
			if nick in omegleSessions:
				omegleSessions[nick].stop()
				del omegleSessions[nick]
#				xmppUtils.sendMessage(sender, sender.getResource() + ": removed - " + nick, type)
			else:
				xmppUtils.sendMessage(sender, "not found - " + nick, 'chat')
			return

		if len(omegleSessions) == 1:
			nick = omegleSessions.keys()[0]
			omegleSessions[nick].stop()
			del omegleSessions[nick]
#			xmppUtils.sendMessage(sender, sender.getResource() + ": removed - " + nick, type)
		else:
			xmppUtils.sendMessage(sender, sender.getResource() + ": stop who?", type)

	elif action == 'skip' or action == 'on' or action == 'next':
		if nick:
			if nick in omegleSessions:
				omegleSessions[nick].stop()
				del omegleSessions[nick]
#				xmppUtils.sendMessage(sender, sender.getResource() + ": removed - " + nick, type)
#			else:
#				xmppUtils.sendMessage(sender, sender.getResource() + ": not found - " + nick, type)

		if not nick:
			if len(omegleSessions) == 1:
				nick = omegleSessions.keys()[0]
				omegleSessions[nick].stop()
				del omegleSessions[nick]
#				xmppUtils.sendMessage(sender, sender.getResource() + ": removed - " + nick, type)
			else:
				nick = getNick(nick)
				if not nick:
					xmppUtils.sendMessage(sender, '.' + sender.getResource() + ": failed to find a random nick", type)
					return

		omegle = OmegleClient(sender.getStripped(), nick)
		omegleSessions[nick] = omegle
		omegle.start()
#		xmppUtils.sendMessage(sender, sender.getResource() + ": added - " + nick, type)

	elif action == 'public' or action == 'private':
		isPublic = (action == 'public')
		if nick and nick in omegleSessions:
				omegleSessions[nick].setScope(isPublic)
				xmppUtils.sendMessage(sender, sender.getResource() + ': switched to ' + action + ' - ' + nick, type)
				return

		if not nick:
			nick = getNick(nick)
			if not nick:
				xmppUtils.sendMessage(sender, sender.getResource() + ": Failed to find a random nick.", type)
				return

		omegle = OmegleClient(sender.getStripped(), nick)
		omegleSessions[nick] = omegle
		omegle.targetHandle = sender.getResource()
		omegle.start(isPublic)
		xmppUtils.sendMessage(sender, sender.getResource() + ': initiated ' + action + ' - ' + nick, type)

	elif action == 'captcha':
		if len(omegleSessions) == 0:
				return

		if not nick or nick not in omegleSessions:
			xmppUtils.sendMessage(sender, sender.getResource() + ': valid nickname required', type)
			return

		if len(args) < 3:
			xmppUtils.sendMessage(sender, sender.getResource() + ': what do I tell them?', type)
			return

		omegleSessions[nick].sendCaptcha(args[2])
		xmppUtils.sendMessage(sender, sender.getResource() + ': sent captcha response - ' + args[2], type)

	elif action == 'list':
		keys = omegleSessions.keys()
		for key in keys:
			if not omegleSessions[key].connected:
				del omegleSessions[key]

		xmppUtils.sendMessage(sender, str(omegleSessions.keys()), 'chat')

	else:
		xmppUtils.sendMessage(sender, "syntax = " + commandText + " (start, stop, skip, public, private, list, captcha) [nickname]", 'chat')