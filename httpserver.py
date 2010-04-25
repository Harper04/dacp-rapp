import storage,httplib,re,urlparse,daap,BaseHTTPServer
from daap import do
import StringIO, md5,struct #hashcode
from threading import Thread

class HTTPServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		url=urlparse.urlparse(self.path)
		params={}
		if(url.query != ''):		
			for c in url.query.split("&"): params[c.split("=")[0]] = c.split("=")[1]
		else: params=None
		if(re.match("/login*",url.path)):self.do_GET_login(params)
		elif(re.match("/server-info*",url.path)): self.do_GET_Server_Info(params)
		elif(params==None and url.path=="/ctrl-int"): self.do_CTRL_INT_S(params)
		elif(self.storage.hasSession(params["session-id"])):#we are logged in
			if(re.match("/update*",url.path)):self.do_GET_Update(params)
			elif(re.match("/databases/1/containers",url.path)):self.do_GET_DATABASES_U(params,url.path,url.query)#pretty static, App supports only one db
			elif(re.match("/databases",url.path)): self.do_GET_DATABASES_S(params)
			elif(re.match("/ctrl-int",url.path)): self.do_CTRL_INT(params,url.path,url.query)
			else:print "Incoming unhandled Request:"+url.path+" with "+url.query
	def do_CTRL_INT(self,params,url,query):
		if(re.match("/ctrl-int/1/getproperty",url)):#okay we want to get something
			if(params["properties"]=="dmcp.volume"):
				cmgt = do('dmap.cmgt',
					[do('dmap.status',200),
					 do('dmap.cmvo',self.storage.getRBVolume())
					])
				self.h(cmgt.encode())
			else: print url+query+" unimplemented"
		elif(re.match("/ctrl-int/1/getspeakers",url)):
			print "getspeakers"
		elif(re.match("setproperty",url)):#okay something to set...
			print url+query+" unimplemented"
		else: print str(url)+query+"What the hack is that!?!"
	def do_CTRL_INT_S(self,params):
		#who knows what that is? sending same as my itunes-...
		if(params==None):
			caci = do('dmap.caci',
					[do('dmap.status',200),
					 do('dmap.updatetype',0),
					 do('dmap.specifiedtotalcount',1),
					 do('dmap.returnedcount',1),
					 do('dmap.listing',
						[do('dmap.listingitem',
							[do('dmap.itemid',1),
							 do('dmap.cmik',1),
							 do('dmap.cmsp',1),
							 do('dmap.cmsv',1),
							 do('cass',1),
							 do('casu',1),
							 do('ceSG',1),
							 ])
						])
					 ])
			self.h(caci.encode())
	def do_GET_DATABASES_U(self,params,path,p):#
		print "unhandled "+path+p
	def do_GET_DATABASES_S(self,params):
		print "Get Databases Query Processing....."
		avdb = do('daap.serverdatabases',
			[do('dmap.status',200),
			 do('dmap.updatetype',0),
			 do('dmap.specifiedtotalcount',1),
			 do('dmap.returnedcount',1),
			 do('dmap.listing',
				[do('dmap.listingitem',
					[do('dmap.itemid',1),
					 do('dmap.persistentid',000001),
					 do('dmap.itemname',str(self.storage.getDBName())),
					 do('dmap.itemcount',1),
					 do('dmap.containercount',3),#fixme, need to get containercount
					 do('dmap.editcommandssupported',1)#??
					])
				])
			])
		self.h(avdb.encode())
	def do_GET_Update(self,params):
		#fixme revision number means the revision of playlists, so when new playlists update etc hang etc
		if(params["revision-number"]==str(1)):
			mupd = do('dmap.updateresponse',
				[do('dmap.status',200),
				 do('dmap.serverrevision',40)])
			self.h(mupd.encode())
	def do_GET_login(self,params):
		if(self.storage.deviceIsKnown(params['pairing-guid'])):
			sID=self.storage.addSession()
			mlog= do('dmap.loginresponse',
				[ do('dmap.status',200),
				  do('dmap.sessionid',sID)
				])
			self.h(mlog.encode())
	def do_GET_Server_Info(self,query):
            print "Sending Server Info"
            msrv = do('dmap.serverinforesponse',
                      [ do('dmap.status', 200),
                        do('dmap.protocolversion', '2.0'),
                        do('daap.protocolversion', '3.0'),
                        do('dmap.timeoutinterval', 1800),
                        do('dmap.itemname', "TomsRB"),
                        do('dmap.loginrequired', 0),
                        do('dmap.authenticationmethod', 0),
                        do('dmap.supportsextensions', 0),
                        do('dmap.supportsindex', 0),
                        do('dmap.supportsbrowse', 0),
                        do('dmap.supportsquery', 0),
                        do('dmap.supportspersistentids', 0),
                        do('dmap.databasescount', 1),                
                        #do('dmap.supportsautologout', 0),
                        #do('dmap.supportsupdate', 0),
                        #do('dmap.supportsresolve', 0),
                       ])
            self.h(msrv.encode())
        def h(self, data, **kwargs):
            self.send_response(kwargs.get('status', 200))
            self.send_header('Content-Type', kwargs.get('type', 'application/x-dmap-tagged'))
            self.send_header('DAAP-Server', 'Simple')
            self.send_header('Expires', '-1')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Language', 'en_us')
            if kwargs.has_key('extra_headers'):
                for k, v in kwargs['extra_headers'].iteritems():
                    self.send_header(k, v)
            try:
                if type(data) == file:
                    self.send_header("Content-Length", str(os.stat(data.name).st_size))
                else:
                    self.send_header("Content-Length", len(data))                   
            except:
                pass
            self.end_headers()
            if hasattr(self, 'isHEAD') and self.isHEAD:
                pass
            else:
                try:
                    if (hasattr(data, 'next')):
                        for d in data:
                            self.wfile.write(d)
                    else:
                        self.wfile.write(data)
                except socket.error, ex:
                    if ex.errno in [errno.ECONNRESET]: pass
                    else: raise
            if (hasattr(data, 'close')):
                data.close()
		
class httpserver(Thread):
	def __init__(self):
		print "started"
		Thread.__init__(self)
	def read(self,queue, size):
		pull = ''.join(queue[0:size])
		del queue[0:size]
		return pull
	def ashex(self,s): return ''.join([ "%02x" % ord(c) for c in s ])
	def asbyte(self,s): return struct.unpack('>B', s)[0]
	def asint(self,s): return struct.unpack('>I', s)[0]
	def aslong(self,s): return struct.unpack('>Q', s)[0]
	def getNewCMPG(self,raw, handle, indent,ntype):
		group =['cmst','mlog','agal','mlcl','mshl','mlit','abro','abar','apso','caci','avdb','cmgt','aply','adbs','cmpa']
		while handle >= 8:
			# read word data type and length
			ptype = self.read(raw, 4)
			plen = self.asint(self.read(raw, 4))
			handle -= 8 + plen
			# recurse into groups
			if ptype in group:
				resulttmp = self.getNewCMPG(raw, plen, indent + 1,ptype)
				if resulttmp != None:
					return resulttmp
				continue
			if (ptype=="cmpg"):
				pdata = self.read(raw, plen)
				result = self.ashex(pdata)
				return result

	def run(self):
		print "runned"
		ex=1
		while ex==1:
			try:
				print "runned"
				self.storage.newServerPort()
				self.server = BaseHTTPServer.HTTPServer(('', self.storage.getServerPort()), HTTPServerHandler)
				ex=0
				print str(self.storage.getServerPort())+"NEW HTTP SERVER"
			except:
				ex=1

		self.server.RequestHandlerClass.storage = self.storage
		self.on=True
		self.storage.setishttpserveron(1)
 		while self.on:
			self.server.handle_request()
		self.server.server_close()
	def stop(self):
		on=False

	def pairRemote(self,address,port,key,pairkey):
		print "G"+address+port+key
		merged = StringIO.StringIO()
		merged.write(pairkey)
		for c in key:  
			merged.write(c)  
			merged.write("\x00") 
		found = (md5.new(merged.getvalue()).hexdigest()).upper()
		
		conn = httplib.HTTPConnection(address+":"+port)
		conn.request("GET","/pair?pairingcode="+found+"&servicename=47975973649ECA79")
		r1 = conn.getresponse()
		print "Pairing: New Message"+str(r1.status)
		if(r1.status==200):
			data = str(r1.read())
			raw = []
			for c in data:raw.append(c)
			d=self.getNewCMPG(raw, len(raw), 0,0)
			print "CMPG                                                 !!!"+d
			self.storage.addNewDevice(d)
		conn.close()
