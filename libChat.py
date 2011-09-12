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

class Client(object):

	def __init__(self):
		self._rooms = {}
		pass
	
	def join(self, room):
		self._rooms[room.getName()] = room
	
	def getRoom(self, name):
		if name not in self._rooms:
			return None
		return self._rooms[room]


class Room(object):

	def __init__(self, client, name):
		self._client = client
		self._name = name
		
		self._roster = dict()
	
	def getClient(self):
		return self._client

	def getName(self):
	  return self._name
	
	def getNick(self):
		return None
	
	def getType(self):
		return None
	
	def getMemberByNick(self, nick):
		nick = nick.lower()
		if nick not in self._roster:
			return None
		return self._roster[nick]
	
	def addMember(self, member):
		nick = member.getNick().lower()
		if nick in self._roster:
			return False
		self._roster[nick] = member
		return True
	
	def removeMember(self, member):
		nick = member
		if isinstance(member, Member):
			nick = member.getNick()
		nick = nick.lower()
		if nick not in self._roster:
			return False
		del self._roster[nick]
		return True


class Member(object):
	
	def __init__(self, room, nick):
		self._room = room
		self._nick = nick
	
	def getNick(self):
		return self._nick

	def getRoom(self):
		return self._room
