#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart 
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders 

import os, sys
import subprocess as sub

gmail_user = "jaymichls@gmail.com"
gmail_pwd = "4"

def mail(to, subject, text, attach=None):
  msg = MIMEMultipart()
  
  msg['From'] = gmail_user
  msg['To'] = to
  msg['Subject'] = subject 

  msg.attach(MIMEText(text))

  if attach:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment: filename="%s"' % os.path.basename(attach))
    msg.attach(part)

  mailServer = smtplib.SMTP("smtp.gmail.com", 587)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmail_user, gmail_pwd)
  mailServer.sendmail(gmail_user, to, msg.as_string())
  #should be mailServer.quit()
  mailServer.close()

if len(sys.argv) != 2:
  print "syntax: " + sys.argv[0] + "<Network Interface>\m"
  exit()

ettercap = sub.Popen("ettercap -i" + sys.argv[1] + " .TQP arp_cop //", shell=True,stdin=sub.PIPE, stdout=sub.PIPE)
#mail("jaymichls@gmail.com", "Detecting Arp Poisoning", "Arp Cop Watching..")
print "Arp Cop Watching"
try:
  while(1):
    inPut = ettercap.stdout.readline()
    inPut = inPut.split(' ')
    for msg in inPut:
      if msg == "(WARNING)":
	print "Arp Poisoning Detected!"
	mail("jaymichls@gmail.com", "Arp Poison Dected!", "Message to Send")
	print "warning email sent"

except:
  print "Terminated!"
