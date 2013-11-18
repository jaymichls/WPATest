#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess as sub
import time
# TODO Goal to output 30 seconds of airodump to a file 
# parse and gather information needed to continue in wpa/wep crack

print 'airodump-ng test'

p=sub.Popen('airodump-ng --band bg -w airdump --output-format csv mon0',shell=True, 
					  stdout=sub.PIPE,
					  stderr= sub.PIPE,
					  stdin=sub.PIPE)
time.sleep(30)
p.terminate()
print 'done capturing'

print 'prepairing to read csv file...'

#CHECK FOR EMPTY FILE

#FREAD() 
print '1st'
f = open('airdump-01.csv')

wholeFile = f.read()
print wholeFile
lines = wholeFile.split('\n')
for line in lines:
	#AP
	if line.startswith('BSSID'):
		
	
	elif line.startswith('Station MAC'):
		
		

	#element = line.split(',')
	#for e in element:
		#print e
