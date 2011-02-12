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

import xmppClient

# TODO: parse config files
# TODO: initialize bot
# TODO: add handlers to bot
# TODO: register commands/plugins
# TODO: add SIGINT and exit handlers
# TODO: loop forever

class Bot:
	client = xmppClient.XMPPConnection("nickel@speeqe.com", "blammo11")
bot = Bot()

bot.client.joinMUC("nick", "pass")

while 1:
	nick=mess.getFrom().getResource()
	text=mess.getBody()
	bot.client.step()
	print "TEXT: " + text
