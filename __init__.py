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
	self.httpserver = httpserver()
	self.httpserver.storage=self.storage
	self.httpserver.start()

	#Unseren Server advertisen
	print
	self.AvahiThreadO = AvahiThread()
	self.AvahiThreadO.storage = self.storage
	self.AvahiThreadO.start()
	print "loel"
	#blah
	self.AvahiThingsO = AvahiThings()
	self.AvahiThingsO.run(shell,self)
	print "lool"

    def deactivate(self, shell):
	self.AvahiThingsO.stop()
	del self.AvahiThingsO
	del self.AvahiThreadO
	self.httpserver.stop()
	del self.httpserver
        del self.shell
