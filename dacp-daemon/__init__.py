import dbus,dbus.service,dbus.glib
import gobject
from dacpdbus import loginClass
from couchdbStorage import CouchStorage
#start dacp-daemon
class initDaemon():
	def initAlltheDBUSInterfaces(self):
		bus = dbus.SessionBus()
		name = dbus.service.BusName("eu.quenyagermany.dacpdaemon",bus=bus)
		obj = loginClass(name,"/")
		obj.Daemon=self
	def initCouchDBAccess(self):
		self.CStorage = CouchStorage()
	def startMainLoop(self):
		self.loop = gobject.MainLoop()
		self.loop.run()

server=initDaemon()
server.initAlltheDBUSInterfaces()
server.initCouchDBAccess()
server.startMainLoop()
