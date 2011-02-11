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

class commandHandler:

	def messageHandler(self, con, msg):
		if msg.getType() != 'groupchat':
			return

		data = msg.getBody()
		nick = msg.getFrom().getResource()
		room = msg.getFrom().getStripped()

		if not nick:
			return

		print msg.getFrom().getResource() + " from " + msg.getFrom().getStripped() + ": " + msg.getBody()

		if len(data) >= 2:
			if data[0] == '!':
				cmds = data[1:].split(' ', 1)
				cmd = cmds[0]
				if cmd in self.commands:
					if len(cmds) == 1:
						cmds.append('')

					priv = self.commands[cmd]['privilege']
					allowed = False

					if not priv:
						allowed = True
					else:
						if (room in self.mucs) and (nick in self.mucs[room]['members']):
							userpriv = self.mucs[room]['members'][nick]['affiliation']

							if priv == 'member':
								if userpriv == 'member' or userpriv == 'admin' or userpriv == 'owner':
									allowed = True
							elif priv == 'admin':
								if userpriv == 'admin' or userpriv == 'owner':
									allowed = True
							elif priv == 'owner':
								if userpriv == 'owner':
									allowed = True

					if allowed:
						self.commands[cmd]['function'](cmds[1])
					else:
						self.errfunc('accessdenied')

			elif data[0] != '.':
				self.msgfunc(msg)

	def presenceHandler(self, con, pres):
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

			if room not in self.mucs:
				self.mucs[room] = {}
				self.mucs[room]['members'] = {}

			if pres.getStatusCode() == '303':
				if nick in self.mucs[room]['members']:
					del self.mucs[room]['members'][nick]
			else:
				if nick not in self.mucs[room]['members']:
					self.mucs[room]['members'][nick] = {}

				self.mucs[room]['members'][nick]['role'] = role
				self.mucs[room]['members'][nick]['affiliation'] = affil
				self.mucs[room]['members'][nick]['status'] = status
				self.mucs[room]['members'][nick]['JID'] = jid
		pass
