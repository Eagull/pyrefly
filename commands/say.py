import xmppUtils

class plugin:
	def execute(self, sender, type, args, client):
		if len(args) > 0:
			room = sender.getStripped()
			xmppUtils.sendMessage(client, room, args, type='groupchat')