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

class Handler(object):
	
	def onRoomJoin(self, room, user):
		pass
	
	def onRoomPart(self, room, user):
		pass
	
	def onRoomNickChange(self, room, user, oldNick):
		pass
	
	def onRoomMessage(self, room, user, message, jid=None):
		pass


class EventBroadcaster(Handler):

	def __init__(self):
		Handler.__init__(self)
		self._handlers = list()
	
	def addHandler(self, handler):
		self._handlers.append(handler)
	
	def removeHandler(self, handler):
		self._handlers.remove(handler)

	def onRoomJoin(self, room, user):
		for handler in self._handlers:
			handler.onRoomJoin(room, user)

	def onRoomPart(self, room, user):
		for handler in self._handlers:
			handler.onRoomPart(room, user)
	
	def onRoomNickChange(self, room, user, oldNick):
		for handler in self._handlers:
			handler.onRoomNickChange(room, user, oldNick)

	def onRoomMessage(self, room, user, message, jid=None):
		for handler in self._handlers:
			handler.onRoomMessage(room, user, message, jid=jid)
