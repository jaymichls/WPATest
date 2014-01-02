#!/usr/bin/python
# -*- coding: utf-8 -*

#Each AP should have a list weither empty or not of all clients associated with the AP	
class AccessPoint:		
	def __init__(self, bssid, channel, encrypt, essid, clientsList=[], numberOfClients=0):
		self.bssid = bssid
		self.channel = channel
		self.encrypt = encrypt
		self.essid = essid
		self.clientsList = clientsList
		self.numberOfClients = numberOfClients
	
	def __dir__(self):
		return 	['numberOfClients','encrypt','channel','bssid', 'essid']
	
	@staticmethod
	def uniqueColumns():
		return ['bssid','essid']

	def addClient(self, client):
		if type(client) is Client:
			self.clientList[self.numberOfClients] = client
			self.numberOfClients += 1
			return 0
		else:
			return -1

class Client:
	def __init__(self, stationMac, bssid):
		self.stationMac = stationMac
		self.bssid = bssid

	def __dir__(self):
		return ['bssid','stationMac']

	@staticmethod
	def uniqueColumns():
		return ['bssid','stationMac']
