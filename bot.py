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

from xmppClient import xmppClient
from handlers import commandHandler

# TODO: parse config files
# TODO: initialize bot
# TODO: add handlers to bot
# TODO: register commands/plugins
# TODO: add SIGINT and exit handlers
# TODO: loop forever


client = xmppClient("jid@example.com/bot", "password")
client.registerHandler('message', commandHandler.messageHandler)
#client.registerHandler('presence', commandHandler.presenceHandler)
#client.registerHandler('message', floodHandler.messageHandler)
#client.registerHandler('presence', floodHandler.presenceHandler)

client.joinMUC("pyrefly", "testmoth@chat.speeqe.com")

while client.step():
	pass