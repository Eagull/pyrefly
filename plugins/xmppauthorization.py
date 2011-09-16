'''
XMPP Bot
Copyright (C) 2011 Eagull.net

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from plugin import Plugin, Authorizer
from libCommand import Command, Help
import re

class XmppAuthorization(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def onLoad(self, bot):
		Plugin.onLoad(self, bot)

	def onUnload(self):
		Plugin.onUnload(self)

	@Authorizer('xmpp')
	def authorize(self, user, role):
		if role == 'member':
			return user.isMember()
		elif role == 'admin':
			return user.isAdmin()
		elif role == 'moderator':
			return user.isModerator()
		elif role == 'owner':
			return user.isOwner()
		return False
	
	@Command('xmpp-auth-check', minArgs=1, maxArgs=1)
	@Help('Check your XMPP auth status', usage='<role>')
	def cmdAuthCheck(self, room, user, args, say, whisper):
		role = args[0]
		if user.isInRole('xmpp', role):
			say("You are authorized for role: xmpp:%s" % role)
		else:
			say("You are not authorized for role: xmpp:%s" % role)
