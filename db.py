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

# Implements a basic non-ACID database against a Google Spreadsheet document.
class Db(object):
	
	# Initialize the database with the given nickname, account, and spreadsheet.
	def __init__(self, nick, email, password, spreadsheetId):
		self.nick = nick
		self.email = email
		self.password = password
		self.spreadsheetId = spreadsheetId
		self.tableIdMap = {}
		self.tableMap = {}
		
	# Connect and log in to Google Spreadsheet service.
	def connect(self):
		self.client = gdata.spreadsheet.service.SpreadsheetsService()
		self.client.email = self.email
		self.client.password = self.password
		self.client.source = self.nick
		self.client.ProgrammaticLogin()
		self._buildTableMap()
	
	# Query and build a map of "tables" (worksheets) to worksheet ids.
	def _buildTableMap(self):
		feed = self.client.GetWorksheetsFeed(self.spreadsheetId)
		for entry in feed.entry:
			table = entry.title.text.lower()
			self.tableIdMap[table] = entry.id.text.rsplit('/', 1)[1]
			self.tableMap[table] = Table(self, table)
	
	# Get a Table object for the given table name.
	def table(self, tableName):
		tableName = tableName.lower()
		if not tableName in self.tableMap:
			return None
		return self.tableMap[tableName]
	
	# Run a query against the database (filtered by the given kvMap), and return a result feed.
	def _query(self, table, kvMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return None
		queryText = " and ".join(["%s=\"%s\"" % (k, v) for k, v in self._clean(kvMap).items()])
		worksheetId = self.tableIdMap[table]
		q = gdata.spreadsheet.service.ListQuery()
		q.sq = queryText
		return self.client.GetListFeed(self.spreadsheetId, worksheetId, query=q)
		
	# Query the given table with the given filter and return a list of results.
	def get(self, table, kvMap):
		table = table.lower()
		feed = self._query(table, kvMap)
		if not feed:
			return []
		results = []
		for entry in feed.entry:
			results.append(self._unclean(dict((v.column, v.text) for v in entry.custom.values())))
		return results
	
	# Query the given table with the given filter and return the first result.
	def getOne(self, table, kvMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return None
		results = self.get(table, kvMap)
		if len(results) == 0:
			return None
		return results[0]
	
	# Query the given table and return a list of all rows.
	def getAll(self, table):
		table = table.lower()
		if not table in self.tableIdMap:
			return None
		worksheetId = self.tableIdMap[table]
		feed = self.client.GetListFeed(self.spreadsheetId, worksheetId)
		results = []
		for entry in feed.entry:
			results.append(self._unclean(dict((v.column, v.text) for v in entry.custom.values())))
		return results
	
	# Insert a row to the given table.
	def put(self, table, vMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		worksheetId = self.tableIdMap[table]
		
		entry = self.client.InsertRow(self._clean(vMap), self.spreadsheetId, self.tableIdMap[table])
		return isinstance(entry, gdata.spreadsheet.SpreadsheetsList)

	# Update rows which match the filter in the given table with a set of changes.
	def update(self, table, kvMap, vMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		feed = self._query(table, kvMap)
		if not feed:
			return False
		
		updateCount = 0
		for entry in feed.entry:
			updateMap = dict()
			for v in entry.custom.values():
				updateMap[v.column] = v.text
			for k, v in vMap.items():
				updateMap[k] = v
			updatedEntry = self.client.UpdateRow(entry, self._clean(updateMap))
			if isinstance(updatedEntry, gdata.spreadsheet.SpreadsheetsList):
				updateCount += 1
		
		return updateCount
		
	# Delete rows that match a filter in the given table
	def delete(self, table, kvMap):
		table = table.lower()
		if not table in self.tableIdMap:
			return False
		
		feed = self._query(table, kvMap)
		if not feed:
			return False
		
		deleteCount = 0
		for entry in feed.entry:
			self.client.DeleteRow(entry)
			deleteCount += 1
		
		return deleteCount
	
	# Sanitize an input dictionary to avoid formula errors.
	# TODO(alx): Base64 encode binary values so the database can store arbitrary info.
	def _clean(self, vMap):
		cleanMap = {}
		for k, v in vMap.items():
			if isinstance(v, unicode):
				v = v.encode('utf-8')
			if v[0:1] in [' ', '$', '@', '=', '<', '>']:
				v = "@%s" % v
			cleanMap[k] = v
		return cleanMap
	
	# Un-sanitize a result from the DB before returning it.
	def _unclean(self, vMap):
		uncleanMap = {}
		for k, v in vMap.items():
			if v is not None:
				if v[0:1] == '@':
					v = v[1:]
			uncleanMap[k] = v
		return uncleanMap
		

class Table(object):
	
	def __init__(self, db, table):
		self.db = db
		self.table = table.lower()
	
	def get(self, kvMap):
		return self.db.get(self.table, kvMap)
	
	def getOne(self, kvMap):
		return self.db.getOne(self.table, kvMap)
	
	def getAll(self):
		return self.db.getAll(self.table)
	
	def update(self, kvMap, vMap):
		return self.db.update(self.table, kvMap, vMap)
	
	def put(self, vMap):
		return self.db.put(self.table, vMap)
	
	def delete(self, kvMap):
		return self.db.delete(self.table, kvMap)
