import xmppUtils
import slap

commandText = 'say'
helpText = 'Write arguments to the standard output.'

def process(sender, type, args, client):
	room = sender.getStripped()
	comSend = sender.getResource()
	room = sender.getStripped()
	if len(args) == 0:
		xmppUtils.sendMessage(room, helpText, type='groupchat')

	elif "!say !say !say" in args:
		xmppUtils.setRole(room, comSend, 'visitor', 'Recursion is not your friend!')
		xmppUtils.sendMessage(room, "Hush, you!", type='groupchat')
	elif "!say !say" in args:
		slap.process(sender, type, comSend, client)
	elif "!say" in args:
		xmppUtils.sendMessage(room, "nou.", type='groupchat')

	else :
		xmppUtils.sendMessage(room, args, type='groupchat')
