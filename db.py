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
		self.tableMap = {}
		
	def connect(self):
		self.client = gdata.spreadsheet.service.SpreadsheetsService()
		self.client.email = self.email
		self.client.password = self.password
		self.client.source = self.nick
		self.client.ProgrammaticLogin()
	
	def openTable(self, tableName, worksheetId):
		self.tableMap[tableName] = worksheetId
	
	def query(self, table, kvMap):
		if not table in self.tableMap:
			return None
		queryText = " and ".join(["%s=\"%s\"" % (k, v) for k, v in kvMap])
		worksheetId = self.tableMap[table]
		q = self.client.ListQuery()
		q.sq = queryText
		return self.client.GetListFeed(self.spreadsheetId, worksheetId, query=q)
		
	def get(self, table, kvMap):
		feed = self.query(table, kvMap)
		if not feed:
			return []
		results = []
		for entry in feed.entries:
			results.push(dict((k, v) for k, v in entry.custom))
		return results
	
	def getOne(self, table, kvMap):
		results = self.get(table, kvMap)
		if len(results) == 0:
			return None
		return results[0]
		
	def put(self, table, vMap):
		if not table in self.tableMap[table]:
			return False
		
		worksheetId = self.tableMap[table]
		
		entry = self.client.InsertRow(vMap, self.spreadsheetId self.tableMap[table]
		return isinstance(entry, gdata.spreadsheet.SpreadsheetsList)

	def update(self, table, kvMap, vMap):
		if not table in self.tableMap:
			return False
		
		feed = self.query(table, kvMap)
		if not feed:
			return False
		
		updateCount = 0
		for entry in feed.entries:
			updatedEntry = self.client.UpdateRow(entry, vMap)
			if isinstance(updatedEntry, gdata.spreadsheet.SpreadsheetsList):
				updateCount++
		
		return updateCount
		
	def delete(self, table, kvMap):
		if not table in self.tableMap:
			return False
		
		feed = self.query(table, kvMap)
		if not feed:
			return False
		
		deleteCount = 0
		for entry in feed.entries:
			self.client.DeleteRow(entry)
			deleteCount++
		
		return deleteCount
		
	
class Table(object):
	
	def __init__(self, db, table):
		self.db = db
		self.table = table
	
	def get(self, kvMap):
		return self.db.get(self.table, kvMap)
	
	def getOne(self, kvMap):
		return self.db.getOne(self.table, kvMap)
	
	def update(self, kvMap, vMap):
		return 
	
	def put(self, vMap):
		return self.db.put(self.table, kVMap)