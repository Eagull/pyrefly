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
		self.tableIdMap = {}
		self.tableMap = {}
		
	def connect(self):
		self.client = gdata.spreadsheet.service.SpreadsheetsService()
		self.client.email = self.email
		self.client.password = self.password
		self.client.source = self.nick
		self.client.ProgrammaticLogin()
		self.buildTableMap()
	
	def buildTableMap(self):
		feed = self.client.GetWorksheetsFeed(self.spreadsheetId)
		for entry in feed.entry:
			table = entry.title.text.lower()
			self.tableIdMap[table] = entry.id.text.rsplit('/', 1)[1]
			self.tableMap[table] = Table(self, table)
	
	def table(self, tableName):
		tableName = tableName.lower()
		if not tableName in self.tableMap:
			return None
		return self.tableMap[tableName]
	
	def query(self, table, kvMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return None
		queryCondList = []
		for k, v in kvMap.items():
			queryCondList.append("%s=\"%s\"" % (k, v))
		queryText = " and ".join(queryCondList)
		worksheetId = self.tableIdMap[table]
		q = gdata.spreadsheet.service.ListQuery()
		q.sq = queryText
		return self.client.GetListFeed(self.spreadsheetId, worksheetId, query=q)
		
	def get(self, table, kvMap):
		table = table.lower()
		feed = self.query(table, kvMap)
		if not feed:
			return []
		results = []
		for entry in feed.entry:
			results.append(dict((v.column, v.text) for v in entry.custom.values()))
		return results
	
	def getOne(self, table, kvMap):
		table = table.lower()
		results = self.get(table, kvMap)
		if len(results) == 0:
			return None
		return results[0]
		
	def put(self, table, vMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		worksheetId = self.tableIdMap[table]
		
		entry = self.client.InsertRow(vMap, self.spreadsheetId, self.tableIdMap[table])
		return isinstance(entry, gdata.spreadsheet.SpreadsheetsList)

	def update(self, table, kvMap, vMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		feed = self.query(table, kvMap)
		if not feed:
			return False
		
		updateCount = 0
		for entry in feed.entry:
			updateMap = dict()
			for v in entry.custom.values():
				updateMap[v.column] = v.text
			for k, v in vMap.items():
				updateMap[k] = v
			updatedEntry = self.client.UpdateRow(entry, updateMap)
			if isinstance(updatedEntry, gdata.spreadsheet.SpreadsheetsList):
				updateCount += 1
		
		return updateCount
		
	def delete(self, table, kvMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		feed = self.query(table, kvMap)
		if not feed:
			return False
		
		deleteCount = 0
		for entry in feed.entry:
			self.client.DeleteRow(entry)
			deleteCount += 1
		
		return deleteCount
		
	
class Table(object):
	
	def __init__(self, db, table):
		self.db = db
		self.table = table.lower()
	
	def get(self, kvMap):
		return self.db.get(self.table, kvMap)
	
	def getOne(self, kvMap):
		return self.db.getOne(self.table, kvMap)
	
	def update(self, kvMap, vMap):
		return self.db.update(self.table, kvMap, vMap)
	
	def put(self, vMap):
		return self.db.put(self.table, vMap)
	
	def delete(self, kvMap):
		return self.db.delete(self.table, kvMap)
