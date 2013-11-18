#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess, os, time


proc = subprocess.Popen('iwconfig', shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout=proc.communicate()[0]
lines=stdout.split('\n')
for line in lines:
   line = line.split()
   if not line.startswith(' '):
	line.split()
	print type(line),line
   if not line.startswith(' ') and line[0:line.find(' ')] != '':
	current_iface=line[0:line.find(' ')]
	print current_iface,'h'
    if line.find('Mode:Monitor') != -1:
	#ifaces.append(current_iface)
	print line
