#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO move the database class to somewhere accessable
	
import dbConnection as dbcon
import WirelessClasses as wc

DATABASE_NAME = 'WpaCrackDB'

def setupDatabase():
	
	wpaCrackDB = dbcon.Database(DATABASE_NAME)

	# Create tables 
	if !dbcon.tableExists(wc.AccessPoint.__class__.name__):
		wpaCrackDB.createTable(wc.AccessPoint.__class__.name__, dir(wc.AccessPoint()), wc.AccessPoint.uniqueColumns())
	if !dbcon.tableExists(wc.Client.__class__.name__):
		wpaCrackDB.createTable(wc.Client.__class__.name__, dir(wc.Client()), wc.Client.uniqueColumns())


