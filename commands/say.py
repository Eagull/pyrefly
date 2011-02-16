from xmpp.protocol import Message

class plugin:
	def execute(self, sender, type, args, client):
		client.send(Message(to=sender.getStripped(), body=args, typ=type))