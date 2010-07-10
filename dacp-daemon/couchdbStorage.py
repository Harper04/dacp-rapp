from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record

class CouchStorage():
	def __init__(self):
		db = CouchDatabase("dacpdaemon",create=True)
