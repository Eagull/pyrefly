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
from handlers import commandHandler, logHandler

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

connResult = client.connect()

if not connResult:
	print "Error connecting to server: " + server
	exit(2)

connResult = client.auth(user, password)

if not connResult:
	print "Error authenticating user: " + user
	exit(3)

client.sendInitPresence()

xmppUtils.client = client

client.RegisterHandler('message', commandHandler.messageHandler)
client.RegisterHandler('presence', xmppUtils.rosterHandler)
client.RegisterHandler('message', logHandler.messageHandler)
client.RegisterHandler('presence', logHandler.presenceHandler)

for room in conf.sections():
	if not '@' in room:
		continue

	if conf.get(room, "nick"):
		nick = conf.get(room, "nick")
	else:
		nick = conf.get("DEFAULT", "nick")

	xmppUtils.joinMUC(nick, room)

# loop forever
while xmppUtils.step():
	pass