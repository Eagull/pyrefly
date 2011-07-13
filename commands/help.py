import xmppUtils

commandText = 'help'
helpText = 'Displays commands available to users.'

def process(sender, type, args, client):
	room = sender.getStripped()
	comSend = sender.getResource()
	if len(args) == 0 and xmppUtils.isAdmin(room, comSend):
		xmppUtils.sendMessage(sender, 'Available commands: help, say, voice, devoice, date, uptime, omegle, quote, act, slap, stab, gift, shoot, scold, google, mode, kick, jid, calc.', type='chat')
	elif len(args) == 0 and xmppUtils.isMember(room, comSend):
		xmppUtils.sendMessage(sender, 'Available commands: help, say, voice, date, uptime, omegle, quote, act, slap, stab, gift, shoot, google, calc.', type='chat')
	elif len(args) == 0 and not xmppUtils.isMember(room, comSend):
		xmppUtils.sendMessage(sender, 'Available commands: help, date, quote.', type='chat')