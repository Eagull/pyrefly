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

import gdata.spreadsheet.service


class Db(object):
	
	def __init__(self, nick, email, password, spreadsheetId):
		self.nick = nick
		self.email = email
		self.password = password
		self.spreadsheetId = spreadsheetId
		self.table_map = {}
		
	def connect(self):
		self.client = gdata.spreadsheet.service.SpreadsheetsService()
		self.client.email = self.email
		self.client.password = self.password
		self.client.source = self.nick
		self.client.ProgrammaticLogin()
	
	def openTable(self, tableName, worksheetId):
		self.table_maps[tableName] = worksheetId
		self.table_feeds[tableName] = self.client.GetListFeed(self.spreadsheetId, worksheetId)
	
	def get(self, table, kvMap):
		if not table in self.table_map:
			return None
		queryText = " and ".join(["%s=\"%s\"" % (k, v) for k, v in kvMap])
		worksheetId = self.table_map[table]
		feed = self.client.GetListFeed(self.spreadsheetId, worksheetId, query=q)
		q = self.client.ListQuery()
		q.sq = queryText
		
		
	def put(self, table, kvMap):
		pass
	
	def update(self, table, kvMap, vMap):
		pass
	
	def delete(self, table, keyName):
		pass
	
class Table(object):
	
	def __init__(self, db, table):
		self.db = db
		self.table = table
	
	def get(self, kvMap):
		return self.db.get(self.table, kvMap)
	
	def put(self, table, kvMap):
		