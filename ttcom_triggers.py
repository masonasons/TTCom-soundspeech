"""Custom TTCom trigger code.

See trigger_cc for details on how to write this module.
This file is not part of TTCom but is loaded by it when found.

Author: Doug Lee
This trigger gives TTCom 3.0 the ability to function as the ttcom 4 fork did. You will get logging support, as well as speech and sounds. You can specify a soundpack in your ttcom.conf file under each server. You can also disable speech and logging on a per server basis by setting speech=False or log=False on a server basis.
"""

import conf
import os
import winsound
import re
from time import time, sleep, strftime
from trigger_cc import TriggerBase

from accessible_output2.outputs import auto
o=auto.Auto()
logpath="logs"
def play(f):
	if os.path.exists(f):
		winsound.PlaySound(f, winsound.SND_ASYNC)

def speak(text,interrupt=False):
	o.braille(text)
	return o.output(text,interrupt)

def write_to_log(worklog, entry):
	f=open(worklog, "a")
	try:
		f.write(entry)
	except:
		pass
	f.close()

def log(name,data):
	if data=="" or data==" ":
		return
	if not os.path.exists("logs"):
		os.makedirs("logs")
	write_to_log(logpath+"/"+name+".log",data+". "+strftime("%c, %x")+"\n")

def output(server,text):
	doSpeak=True
	doLog=True
	doInterrupt=False
	speaking=""
	interrupting=""
	logging=""
	for shortname,pairs in conf.conf.servers().items():
		if server.shortname==shortname:
			for k,v in pairs:
				if k=="speech":
					speaking=v
				if k=="interrupt":
					interrupting=v
				if k=="log":
					logging=v
	if speaking.lower()=="false":
		doSpeak=False
	if interrupting.lower()=="true":
		doInterrupt=True
	if logging.lower()=="false":
		doLog=False

	if doSpeak==True:
		speak(server.shortname+" "+text,doInterrupt)
	if doLog==True:
		log(server.shortname,text)

class Trigger(TriggerBase):
	def __init__(self, *args, **kwargs):
		super(Trigger, self).__init__(*args, **kwargs)
		self.soundpack=""
		self.blindyTrigger()

	def serverIsCurrent(self):
		"""Returns True if this trigger is from the server that is current.
		"""
		return self.server == self.server.parent.curServer

	def blindyTrigger(self):
		if not self.server.loggedIn: return
		self.soundpack=""
		for shortname,pairs in conf.conf.servers().items():
			if self.server.shortname==shortname:
				for k,v in pairs:
					if k=="soundpack":
						self.soundpack=v
		if self.soundpack=="":
			self.soundpack="masonasons"
		if self.server.me.userid==self.event.parms.userid: return
		if self.event.event in ["loggedin"]:
			play("sounds/"+self.soundpack+"/in.wav")
			output(self.server,self.server.nonEmptyNickname(self.event.parms.userid, False, True, shortenFacebook=True)+" logged in.")
		elif self.event.event in ["loggedout"]:
			play("sounds/"+self.soundpack+"/out.wav")
			output(self.server,self.server.nonEmptyNickname(self.event.parms.userid, False, True, shortenFacebook=True)+" logged out.")
		elif self.event.event in ["messagedeliver"]:
			if self.event.parms.type==1:
				play("sounds/"+self.soundpack+"/user.wav")
			else:
				play("sounds/"+self.soundpack+"/channel.wav")
			output(self.server,self.server.nonEmptyNickname(self.event.parms.srcuserid, False, True, shortenFacebook=True)+": "+self.event.parms.content)
		elif self.event.event in ["adduser"]:
			play("sounds/"+self.soundpack+"/join.wav")
			output(self.server,self.server.nonEmptyNickname(self.event.parms.userid, False, True, shortenFacebook=True)+" joined "+self.server.channelname(self.event.parms.channelid).strip("/"))
		elif self.event.event in ["removeuser"]:
			play("sounds/"+self.soundpack+"/leave.wav")
			output(self.server,self.server.nonEmptyNickname(self.event.parms.userid, False, True, shortenFacebook=True)+" left "+self.server.channelname(self.event.parms.channelid).strip("/"))
		elif self.event.event in ["updateuser"]:
			play("sounds/"+self.soundpack+"/status.wav")
			what=""
			if "nickname" in self.event.parms:
				what="Changed their nickname"
				output(self.server,self.server.nonEmptyNickname(self.event.parms.userid, False, True, shortenFacebook=True)+" "+what)