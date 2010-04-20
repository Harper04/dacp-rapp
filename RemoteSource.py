# -*- coding: utf-8 -*-

# RemoteSource.py
#
# Copyright (C) 2007 - Guillaume Desmottes
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Parts from "Magnatune Rhythmbox plugin" (stolen from rhythmbox's MagnatuneSource.py)
#     Copyright (C), 2006 Adam Zimmerman <adam_zimmerman@sfu.ca>
import httpserver
import rb, rhythmdb

import os
import gobject
import gtk
import gnome, gconf
import xml
import gzip
import datetime
import storage

class RemoteSource(rb.Source):
	__gproperties__ = {
		'plugin': (rb.Plugin, 'plugin', 'plugin', gobject.PARAM_WRITABLE|gobject.PARAM_CONSTRUCT_ONLY),
	}

	def __init__(self):
	        rb.Source.__init__(self, name=_("Remote App"))
	        self.__activated = False
		print " REMOTESOURCE!!! ! ! !  ! ! ! ! "

		#rb.BrowserSource.__init__(self, name=_("Remote"))
	def do_impl_activate(self):
		if not self.__activated:
			self.__activated = True
		label = gtk.Label("Bitte geben Sie den 5 stelligen Key ein!:")
		label.show()
		self.pack_start(label)
		self.text = gtk.Entry()
                self.pack_start(self.text,gtk.FALSE, gtk.FALSE, 0)
		self.text.show()
	        button = gtk.Button("Pairen")
		print self.storage
	        button.connect("clicked", self.button_clicked)
	        button.show()
	        self.pack_end(button)

		self.show()
	        rb.Source.do_impl_activate (self)
	def button_clicked(self,data):
		self.httpserver.pairRemote(self.address,self.port,self.text.get_text(),self.pairkey)
        def do_impl_delete_thyself(self):
		rb.Source.do_impl_delete_thyself (self)


gobject.type_register(RemoteSource)

