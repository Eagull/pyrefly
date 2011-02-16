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

import xmpp;
import xmppClient;
from commands import say

commands = {'say': say.plugin()}
mucs = {}

def messageHandler(con, msg):
	print '[%s] <%s> %s' % (msg.getType(), msg.getFrom(), msg.getBody())

	data = msg.getBody()
	nick = msg.getFrom().getResource()

	if not nick:
		return

	if len(data) >= 2 and data[0] == '!':
		argSplit = data[1:].split(' ', 1)
		command = argSplit[0]
		args = argSplit[1] if len(argSplit) == 2 else '';
		if command in commands:
			commands[command].execute(msg.getFrom(), msg.getType(), args, con);

def presenceHandler(con, pres):
	MUC = False
	for tag in pres.getTags('x'):
		ns = tag.getNamespace()
		if ns.startswith(xmpp.NS_MUC):
			MUC = True

	if MUC:
		room = unicode(pres.getFrom())
		nick = room[room.find('/') + 1:]
		room = room[:room.find('/')]

		type = pres.getType()
		role = pres.getRole()
		affil = pres.getAffiliation()
		status = pres.getStatus()
		jid = pres.getJid()

		if room not in mucs:
			mucs[room] = {}
			mucs[room]['members'] = {}

		if pres.getStatusCode() == '303':
			if nick in mucs[room]['members']:
				del mucs[room]['members'][nick]
		else:
			if nick not in mucs[room]['members']:
				mucs[room]['members'][nick] = {}

			mucs[room]['members'][nick]['role'] = role
			mucs[room]['members'][nick]['affiliation'] = affil
			mucs[room]['members'][nick]['status'] = status
			mucs[room]['members'][nick]['JID'] = jid
	pass