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
import ConfigParser

import xmppUtils
from handlers import commandHandler

# TODO: register commands/plugins
# TODO: add SIGINT and exit handlers

# parse config files
botConf = "bot.conf"

conf = ConfigParser.RawConfigParser()
conf.read(botConf)

jid = xmpp.JID(conf.get("DEFAULT", "id"))
user = jid.getNode()
server = jid.getDomain()
password = conf.get("DEFAULT", "password")

# initialize bot
client = xmpp.Client(server, debug=[]);

res = client.connect()

if not res:
	print "Error connecting to server: " + server
	exit(2)

res = client.auth(user, password)

if not res:
	print "Error authenticating user: " + user
	exit(3)

client.sendInitPresence()

# add handlers to bot
client.RegisterHandler('message', commandHandler.messageHandler)
#client.registerHandler('presence', commandHandler.presenceHandler)
#client.registerHandler('message', floodHandler.messageHandler)
#client.registerHandler('presence', floodHandler.presenceHandler)

for room in conf.sections():
	if conf.get(room, "nick"):
		nick = conf.get(room, "nick")
	else:
		nick = conf.get("DEFAULT", "nick")

	xmppUtils.joinMUC(client, nick, room)

# loop forever
while xmppUtils.step(client):
	pass