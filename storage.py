import gconf,random
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import rb, rhythmdb

class storage():
	def __init__(self):
		self.client = gconf.client_get_default()
		self.client.add_dir("/apps/rhythmbox/plugins/dacp-rapp",gconf.CLIENT_PRELOAD_NONE)
		self.devices_string = str(self.client.get_string("/apps/rhythmbox/plugins/dacp-rapp/devices"))
		
		#parse devices into list
		self.devices_list = self.devices_string.split(";")
		self.sessions = []
		self.port=1500
		self.HTTPServer=0
	def run(self):
		print "Storage is Up"
	def setishttpserveron(self,what): self.HTTPServer=1
	def ishttpserveron(self): return self.HTTPServer
	def getServerPort(self):return self.port
	def newServerPort(self): self.port=self.port+1
	def deviceIsKnown(self,cmpg):
		number = self.devices_list.count(cmpg)
		if number == 0:
			return False
		else:
			return True

	def addNewDevice(self,cmpg):
		print "adding device"+str(cmpg)
		self.devices_string = self.devices_string+";0x"+(str(cmpg)).upper()
		self.client.set_string("/apps/rhythmbox/plugins/dacp-rapp/devices",self.devices_string)
		self.devices_string = self.client.get_string("/apps/rhythmbox/plugins/dacp-rapp/devices")
		#parse devices into list
		self.devices_list = self.devices_string.split(";")
	def addSession(self):
		x=random.randint(10000000,19999999)
		print "NewSession"+str(x)
		self.sessions.append(x)
		return x
	def removeSession(self,session):
		self.sessions.remove(session)
	def hasSession(self,session):
		if int(session) in self.sessions:
			return True
		else:
			return False
	def getDBName(self):
		return "Harper RB DB"

	def isplaying(self): 
		try: 
			self.player.get_playing_time()
			return True
		except:
			return False
	def ispaused(self):
		try:
			if(self.player.get_playing()):
				return False
			else: 
				self.isplaying()
				return True
		except:
			return False
	def isshuffleactive(self): return self.player.get_playback_state()[0]
	def isrepeatactive(self):  return self.player.get_playback_state()[1]
	def getRBVolume(self):
		return int(self.player.get_volume()*100)
	def getNowPlayingInformation(self):
		entry=self.player.get_playing_entry()
		time=int(self.player.get_playing_time())*1000
		time_total=int(self.player.get_playing_song_duration())*1000
		return [self.getSongInfo(entry),time,time_total]
	def getSongInfo(self,entry):
		title = str(self.db.entry_get(entry,rhythmdb.PROP_TITLE))
		artist = str(self.db.entry_get(entry,rhythmdb.PROP_ARTIST))
		album = str(self.db.entry_get(entry,rhythmdb.PROP_ALBUM))
		entry_id = int(str(self.db.entry_get(entry,rhythmdb.PROP_ENTRY_ID)))
		genre = str(self.db.entry_get(entry,rhythmdb.PROP_GENRE))		
		return [entry_id,title,artist,album,genre]
