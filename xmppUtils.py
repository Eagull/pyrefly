'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.	If not, see <http://www.gnu.org/licenses/>.
'''

from xmpp.protocol import NS_MUC_USER, Iq, NS_MUC_ADMIN, JID
import xmpp

nicks = {}
rosters = dict()
joining = []
client = None

def setClient(clientObj):
	global client
	client = clientObj
	client.nicks = nicks
	client.rosters = rosters

def joinMUC(nick, muc, password=''):
	joining.append(muc)
	rosters[muc] = {}
	nicks[muc] = nick
	presence = xmpp.Presence(to=muc + '/' + nick)
	presence.setTag('x', namespace=xmpp.NS_MUC).setTagData('password', password)
	presence.getTag('x').addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
	client.send(presence)

def sendMessage(jid, message, type='chat'):
	if type == 'groupchat':
		jid = JID(jid).getStripped()
	string = '[%s] <me> %s' % (type[:1], repr(message))
	print string.encode('utf-8') # unicode fix #
	message = xmpp.protocol.Message(to=jid, body=message, typ=type)
	client.send(message)

def setRole(room, nick, role, reason=''):
	iq = Iq('set', NS_MUC_ADMIN, {}, room)
	item = iq.getTag('query').setTag('item')
	item.setAttr('nick', nick)
	item.setAttr('role', role)
	if reason: item.addChild('reason', {}, reason)
	client.send(iq)

def setAffiliation(room, nick, affiliation, reason=''):
	iq = Iq('set', NS_MUC_ADMIN, {}, room)
	item = iq.getTag('query').setTag('item')
	item.setAttr('nick', nick)
	item.setAttr('affiliation', affiliation)
	if reason: item.addChild('reason', {}, reason)
	client.send(iq)

def isModerator(muc, nick):
	if not nick in rosters[muc]: return 0
	return rosters[muc][nick][1] == 'moderator'

def isMember(muc, nick):
	if not nick in rosters[muc]: return 0
	return rosters[muc][nick][0] in ['member', 'admin', 'owner']

def isAdmin(room, nick):
	if not nick in rosters[room]: return 0
	return rosters[room][nick][0] in ['admin', 'owner']

def isOwner(room, nick):
	if not nick in rosters[room]: return 0
	return rosters[room][nick][0] == 'owner'

def rosterHandler(sess, pres):
	nick = pres.getFrom().getResource()
	muc = pres.getFrom().getStripped()

	# if not from one of the joined MUCs, return
	if not muc in nicks:
		return

	if pres.getType() == 'unavailable':
		if nick in rosters[muc]:
			x = pres.getTag('x', {}, NS_MUC_USER)
			item = x.getTag('item')
			status = x.getTag('status')
			if status and status.getAttr('code') == '303':
				newnick = item.getAttr('nick')
				#print 'DEBUG: '+nick+' is now known as '+newnick
				rosters[muc][newnick] = rosters[muc][nick]

				if nicks[muc] == nick: nicks[muc] = newnick
				#print 'DEBUG: myself, '+nick+' is now known as '+newnick

			del rosters[muc][nick]
	else:
		status = 'online'
		show = pres.getTag('show')
		if show: status = show.getData()
		statusnode = pres.getTag('status')
		if statusnode:
			msg = statusnode.getData()
			p = msg.find('\n')
			if p != -1: msg = msg[:p] + ' [...]'
			if len(msg) > 70: msg = msg[:64] + ' [...]'
			status += ' (' + msg + ')'

		if nick in rosters[muc]:
			rosters[muc][nick][3] = status

		x = pres.getTag('x', {}, NS_MUC_USER)
		item = x.getTag('item')
		if item:
			aff = item.getAttr('affiliation')
			role = item.getAttr('role')
			jid = item.getAttr('jid')

			rosters[muc][nick] = [aff, role, jid, status]

		if nick == nicks[muc]:
			if muc in joining: joining.remove(muc)