#!/usr/bin/python
# -*- coding: utf-8 -*-
class AccessPoint:
	
	def __init__ (self,  bssid, channel, encrypt, essid):
		self.bssid = bssid
		self.bssid = channel
		self.encrypt = encrypt
		self.clientsList = []
		self.numberOfClients = 0
	
	def toString(self):
		print 'ESSID: ' + self.essid
		
	def addClient(self, client):
		self.clientsList.append(client)
		self.numberOfClients = self.numberOfClients + 1
		
class Database:
	import sqlite3 as lite
	con = None
	# TODO: Add error handleing on connection checks 
	
	def __init__(self, database):
		self.database = database
		connectToDB(self, self.database)
		#createTables(self)
		
	def connectToDB(self, database):
		if self.con:
			return

		try:
			self.con = lite.connect(database)
			
		except lite.Error, e:
			
			print "SQL Error %s:" % e.args[0]
	
	def closeDB(self):
			if self.con:
				con.close()
	
	def createTables(self):
		createAccessPointsTable(self)
		print 'Tables successfully created'
	
	def createTable(self, tableName, listOfColsAndTypes, colsAndTypes):
		# TODO: Create a table given the table name and the columns and column types.
		# maybe pass colname type as a string need to be separated by ','
		if self.con:
			with self.con:
				cur = self.con.cursor()
				cur.execute("CREATE TABLE %s(%s)"%s(tableName, colsAndTypes))
	
	def createAccessPointsTable(self):
		# TODO: add check to see if table has already been created
		if self.con:
			with self.con:
				
				cur = self.con.cursor()    
				cur.execute("CREATE TABLE AccessPoints(bssid TEXT, essid TEXT, encrypt TEXT, channel INT)")
				
	# can this be generalized?
	def saveAccessPoint(self, ap):
		# TODO: add a last seen date.  
		# If the entry is already in the table update it, don't add duplicated entries.
		if con:
			with con:
				cur = con.cursor()
				cur.execute("INSERT INTO AccessPoints VALUES(%s, %s, %s, %d)"%(ap.bssid, ap.essid, ap.encrypt, ap.channel))
			
	
	def getAccessPoint(self, bssid):
		if con:
			with con:    
				cur = con.cursor()    
				cur.execute("SELECT * FROM AccessPoints WHERE bssid LIKE %s"%(bssid))

			rows = cur.fetchall()
			# TODO return something...
			for row in rows:
					print "%s %s %s %s" % (row["essid"], row["bssid"], row["encrypt"], row["channel"])
			
# Saves Access Point information 
def storeAccessPoint(ap):
	
	con.saveAccessPoint(ap)
		
# Attempt to load Access Point saved data
def loadAccessPoint(ap):
	
	foundAp = getAccessPoint(ap.bssid)
	
def setup():
	#Check if there is already a database file, Other wise create a new one
	db = DB('access_points')
	



