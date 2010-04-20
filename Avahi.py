from dbus.mainloop.glib import DBusGMainLoop
import rb,gtk
import os
from threading import Thread
import avahi,dbus,dbus.glib,dbus.service,gobject
from RemoteSource import RemoteSource
import httpserver,storage

class AvahiThread(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		#str(self.storage.getServerPort())
		os.system('avahi-publish -s 47975973649ECA79 _touch-able._tcp 1500 Ver=131072 DvSv=1905 DbId=47975973649ECA7B DvTy=iTunes OSsi=0xD97F txtvers=1 CtlN=Harper')


class AvahiThings():
	def newRemote(self,interface,protocol,name,stype,domain,flags):
		print "ADDED"+str(interface)+" "+str(protocol)+" "+str(name)+" "+str(stype)+" "+str(domain)+" "+str(flags)
		dbusinfos = self.server.ResolveService(int(interface),int(protocol),str(name),str(stype),str(domain),0,0)
                self.source = gobject.new (RemoteSource,
                                           shell=self.shell,
                                           entry_type=self.entry_type,
                                           plugin=self.rbplugin,
                                           icon=self.icon,
                                           source_group=self.group)
		self.source.address = str(dbusinfos[7])
		self.source.port    = str(dbusinfos[8])
		self.source.pairkey = ((str(avahi.txt_array_to_string_array(dbusinfos[9])[4])).split("="))[1]
		self.source.remotename = name
		self.source.storage = self.rbplugin.storage
		self.source.httpserver = self.rbplugin.httpserver
                self.shell.register_entry_type_for_source(self.source, self.entry_type)
                self.shell.append_source(self.source, None) # Add the source to the list


	def RemoteRemoved(self,interface,protocol,name,stype,domain,flags):
		print "REMOVED"+name
		self.source.delete_thyself()
                self.source = None

	def run(self,rbshell,rbplugin):
		print "Avahi THINGS !!!!!!!!!!!!!!"
		self.shell=rbshell
		self.rbplugin=rbplugin

		#GUI allgemein vorbereiten
		self.db = self.shell.get_property("db")
		self.entry_type = self.db.entry_register_type("RemoteEntryType")
		self.entry_type.can_sync_metadata = True
                self.entry_type.sync_metadata = None
                theme = gtk.icon_theme_get_default()
                rb.append_plugin_source_path(theme, "/icons/")
                width, height = gtk.icon_size_lookup(gtk.ICON_SIZE_LARGE_TOOLBAR)
                self.icon = rb.try_load_icon(theme, "jamendo", width, 0)
                self.group = rb.rb_source_group_get_by_name ("stores")

		#DBUS lauschen auf remotes
		bus=dbus.SystemBus()#mainloop=loop)
		self.server = dbus.Interface(bus.get_object('org.freedesktop.Avahi','/'),"org.freedesktop.Avahi.Server")
		b = dbus.Interface(bus.get_object(avahi.DBUS_NAME,self.server.ServiceBrowserNew(avahi.IF_UNSPEC,avahi.PROTO_UNSPEC,"_touch-remote._tcp", 'local', dbus.UInt32(0))),avahi.DBUS_INTERFACE_SERVICE_BROWSER)
		b.connect_to_signal("ItemNew",self.newRemote)
		b.connect_to_signal("ItemRemove",self.RemoteRemoved)



		#DBUS END

	def stop(self):
		#Remove GUI
                self.action_group = None
                self.db.entry_delete_by_type(self.entry_type)
                self.db.commit()
                self.db = None
                self.entry_type = None
		self.server = None

