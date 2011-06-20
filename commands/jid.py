import xmppUtils

commandText =   'jid'
helpText	=  "Displays a member's JID, so they don't hurt"

def process(sender, type, args, client):
	if len(args) > 0:
		room = sender.getStripped()
		if room in xmppUtils.rosters:
			if args in xmppUtils.rosters[room]:
				jid = xmppUtils.rosters[room][args] [2]
				xmppUtils.sendMessage(sender, jid, type)


