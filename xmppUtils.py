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

class XmppUtil(object):
  
  def __init__(self, client):
    self.client = client
    self.myNick = dict()
    self.rosters = dict()
    self.joining = list()
    
  def joinMUC(self, nick, muc, password=''):
    self.joining.append(muc)
    self.rosters[muc] = dict()
    self.myNick[muc] = nick
    
    roomId = '%s/%s' % (muc, nick)
    
    presence = xmpp.Presence(to=roomId)
    x = presence.setTag('x', namespace=xmpp.NS_MUC)
    x.setTagData('password', password)
    x.addChild('history', {'maxchars': '0', 'maxstanzas': '0'});
    self.client.send(presence)

  def sendMessage(self, jid, message, type):
    # Log the outgoing message.
    log = u'[%s] <me> %s' % (type[:1], message)
    print log.encode('utf-8')
    
    message = xmpp.protocol.Message(to=jid, body=message, type=type)
    self.client.send(message)
    
  def sendMUCMessage(self, jid, message):
    self.sendMessage(JID(jid).getStripped(), message, 'groupchat')
  
  def sendPrivateMessage(self, jid, message):
    self.sendMessage(jid, message, 'chat')
  
  def setRole(self, muc, nick, role, reason=''):
    iq = Iq('set', NS_MUC_ADMIN, {}, muc)
    item = iq.getTag('query').setTag('item')
    item.setAttr('nick', nick)
    item.setAttr('role', role)
    if reason:
      item.addChild('reason', {}, reason)
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