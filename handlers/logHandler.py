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

def messageHandler(client, msg): # Now with 50% more try: !
	if msg.getBody():
		try:
			print '[%s] <%s> %s' % (msg.getType()[:1], msg.getFrom(), msg.getBody())
		except UnicodeEncodeError:
			string = '[%s] <%s> %s' % (msg.getType()[:1], msg.getFrom(), msg.getBody())
			print string.encode('utf-8')

def presenceHandler(client, pres): # Now with 50% more try:

	try:
		print pres
	except UnicodeEncodeError:
		string = pres
		try:
			print string.encode('utf-8')
		except AttributeError:
			pass

#	MUC = False
#	for tag in pres.getTags('x'):
#		ns = tag.getNamespace()
#		if ns.startswith(xmpp.NS_MUC):
#			MUC = True
#
#	if MUC:
#		room = unicode(pres.getFrom())
#		nick = room[room.find('/') + 1:]
#		room = room[:room.find('/')]

#		type = pres.getType()
#		role = pres.getRole()
#		affil = pres.getAffiliation()
#		status = pres.getStatus()
#		jid = pres.getJid()