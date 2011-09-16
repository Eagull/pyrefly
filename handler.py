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
	
	def onError(self, handler, err, room=None):
		return False


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
			try:
				handler.onRoomJoin(room, user)
			except Exception as err:
				if not handler.onError('onRoomJoin', err, room=room):
					raise

	def onRoomPart(self, room, user):
		for handler in self._handlers:
			try:
				handler.onRoomPart(room, user)
			except Exception as err:
				if not handler.onError('onRoomPart', err, room=room):
					raise
	
	def onRoomNickChange(self, room, user, oldNick):
		for handler in self._handlers:
			try:
				handler.onRoomNickChange(room, user, oldNick)
			except Exception as err:
				if not handler.onError('onRoomNickChange', err, room=room):
					raise

	def onRoomMessage(self, room, user, message, jid=None):
		for handler in self._handlers:
			try:
				handler.onRoomMessage(room, user, message, jid=jid)
			except Exception as err:
				if not handler.onError('onRoomMessage', err, room=room):
					raise
