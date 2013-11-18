#!/usr/bin/python
# -*- coding: utf-8 -*-

print 'prepairing to read csv file...'
#CHECK FOR EMPTY FILE
#Each AP requires to store  BSSID, CHANNEL, ENCRYPTION, ESSID
class AP:		
	def __init__(self, bssid, channel, encrypt, essid):
		self.bssid = bssid
		self.channel = channel
		self.encrypt = encrypt
		self.essid = essid
		
	def info(self):
		print self.essid
#FREAD() 
f = open('airdump-01.csv')

wholeFile = f.read()
#print wholeFile
lines = wholeFile.split('\n')

#if the line starts with bssid or a space go to the next line
#strip the info once the line starts with station mac exit.
allAPS = []
for line in lines:
	#AP
	if line.startswith('BSSID,') or line.startswith(' '):
		continue
		
	else:
		if line.startswith('Station MAC'):
			break
		#strip the the line and get required data.
		l = line.split(',')
		if len(l) <= 1:
			continue
		bssid = l[0]
		channel = l[3]
		encrypt = l[5]
		essid = l[13]
		#make a new ap object
		ap = AP(bssid, channel, encrypt, essid)
		#add to list of 
		allAPS.append(ap)
		#print essid
i=1
for a in allAPS:
	print '%d.'%(i),str.strip(a.essid)
	i+=1

