'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xmpp
import config

import xmppUtils
from handlers import commandHandler, logHandler, fightHandler, swearHandler, replyHandler
import pyrefight
import dictionary

# TODO: add SIGINT and exit handlers

jid = xmpp.JID(config.get("id"))

# initialize bot
client = xmpp.Client(jid.getDomain(), debug=[]);
connResult = client.connect()
if not connResult:
	print "Error connecting to server: " + jid.getDomain()
	exit(2)

resource = 'bot' + config.hash[:6]

connResult = client.auth(jid.getNode(), config.get("password"), resource)
if not connResult:
	print "Error authenticating user: " + jid.getNode()
	exit(3)

client.sendInitPresence()

xmppUtils.setClient(client)

#~ client.RegisterHandler('message', logHandler.messageHandler)
client.RegisterHandler('presence', logHandler.presenceHandler)
client.RegisterHandler('presence', xmppUtils.rosterHandler)
client.RegisterHandler('message', commandHandler.messageHandler)

client.RegisterHandler('message', replyHandler.messageHandler)
client.RegisterHandler('message', swearHandler.messageHandler)

#~ client.RegisterHandler('message', fightHandler.messageHandler)
#~ client.RegisterHandler('presence', pyrefight.presHandler)

for room in config.getRoomList():
	nick = config.get("nick", room)
	xmppUtils.joinMUC(nick, room)

# loop forever
try:
	while client.Process(0.1):
		pass
except KeyboardInterrupt:
	exit(0)