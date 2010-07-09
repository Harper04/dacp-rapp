import httpserver
import rhythmdb, rb
import gobject
import gtk
from RemoteSource import RemoteSource
from storage import storage
from httpserver import httpserver
from Avahi import AvahiThread,AvahiThings

class dacprapp (rb.Plugin):
    def __init__(self):
        rb.Plugin.__init__(self)

    def activate(self, shell):
        self.shell = shell
	self.storage = storage()
	self.storage.shell = self.shell
	self.storage.player = self.shell.get_player()
	self.storage.db = self.shell.props.db

	self.httpserver = httpserver()
	self.httpserver.storage=self.storage
	self.httpserver.start()

	#Unseren Server advertisen
	self.AvahiThreadO = AvahiThread()
	self.AvahiThreadO.storage = self.storage
	self.AvahiThreadO.start()
	#blah
	self.AvahiThingsO = AvahiThings()
	self.AvahiThingsO.run(shell,self)

    def deactivate(self, shell):
	self.AvahiThingsO.stop()
	del self.AvahiThingsO
	del self.AvahiThreadO
	self.httpserver.stop()
	del self.httpserver
        del self.shell
