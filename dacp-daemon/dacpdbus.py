#Classes for dbus communication
import dbus,dbus.service,dbus.glib
import gobject

class loginClass(dbus.service.Object):

	@dbus.service.method(dbus_interface="eu.quenyagermany.dacpdaemon",in_signature="v",out_signature="s")
	def login(self,variant):
		return str(variant)
