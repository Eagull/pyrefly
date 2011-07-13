import xmppUtils

commandText = 'act'
helpText = 'Makes the bot do things in third person.'

def process(sender, type, args, client):
	room = sender.getStripped()
	if len(args) == 0:
		xmppUtils.sendMessage(room, helpText, type='groupchat')
	elif len(args) > 0:
		room = sender.getStripped()
		act = '/me ' + args
		xmppUtils.sendMessage(room, act, type='groupchat')
