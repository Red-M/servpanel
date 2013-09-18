import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
import ast
import os
import sys
import time
import json
import socket
import hashlib
from multiprocessing import Process, Pipe

current_dir = os.path.dirname(os.path.abspath(__file__))
if os.name == 'posix':
    lookup = TemplateLookup(directories=[current_dir+'/templates'])
if os.name == 'nt':
    lookup = TemplateLookup(directories=[current_dir+'\\templates'])
    
class Bunch(dict):
    def __init__(self, d):
        dict.__init__(self, d)
        self.__dict__.update(d)

def to_bunch(d):
    r = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = to_bunch(v)
        r[k] = v
    return Bunch(r)
    
def serve_template(tmpl, **kwargs):
    """ loads a template and renders it """
    tmpl = lookup.get_template(tmpl)
    return tmpl.render(**kwargs)
    
def client(ip, port, message):
    if not (socket.getdefaulttimeout()==0.75):
        socket.setdefaulttimeout(0.75)
    sock = socket.create_connection((ip, port),timeout=0.75)
    try:
        sock.sendall(message)
        data = {}
        data = ast.literal_eval(sock.recv(1024*16).replace("\\%s" % ("\\"), \
                                                                        "\\"))
    finally:
        sock.close()
        return data
        
def dataget(conn,hashedauth,bot,data,input):
    #print(socket.getdefaulttimeout())
    auth = hashedauth[data]
    try:
        input[data] = client(bot.config["Servers"][data]["ip"], \
        int(bot.config["Servers"][data]["port"]), \
        auth)
    except Exception,e:
        input[data] = e
    conn.send(input[data])
    conn.close()
        
class StatusPage:
    @cherrypy.expose
    def index(self):
        input = {}
        outdata = []
        p = {}
        parconn = {}
        chiconn = {}
        for data in sorted(bot.config["Servers"]):
            parconn[data], chiconn[data] = Pipe()
            p[data] = Process(target=dataget, args=(chiconn[data],hashedauth,bot,data,input))
            p[data].start()
        for data in sorted(bot.config["Servers"]):
            input[data] = parconn[data].recv()
            p[data].join()
        cluster = 0
        clusters = 0
        stats = []
        for inpdata in sorted(input):
            cluster+=1
            #print(type(input[inpdata]))
            if (type(input[inpdata])==type({})):
                outer = ""
                for odata in sorted(input[inpdata]):
                    if odata=="RAM" or odata=="SWAP":
                        outer=outer+"<p><b>"+odata+"</b>: "+input[inpdata][odata]+" MB</p>"
                    else:
                        outer=outer+"<p><b>"+odata+"</b>: "+input[inpdata][odata]+"</p>"
                outdata.append("<h2>"+inpdata+'    <span class="label label-success">Online</span></h2>\n'+outer)
            else:
                if (str(input[inpdata])=="[Errno 111] Connection refused"):
                    outdata.append("<h2>"+inpdata+'    <span class="label label-success">Online<span class="label label-important"><span title="The Server is Online but the ServPanel Client is not running or the ServPanel Client is not running on the port defined in the config."><b>!!</b></span></span></span></h2>'+str(input[inpdata]))
                else:
                    outdata.append("<h2>"+inpdata+'    <span class="label label-failure">Offline</span></h2>'+str(input[inpdata]))
            if cluster==(len(bot.config["Servers"])/3):
                cluster = 0
                clusters += clusters
                if clusters==len(bot.config["Servers"]):
                    outdata[len(outdata)-1] = outdata[len(outdata)-1]+'</div>\n'
                else:
                    outdata[len(outdata)-1] = outdata[len(outdata)-1]+'</div>\n        <div class="span4">'
                for cludata in xrange(0,len(outdata)):
                    stats.append(outdata[cludata])
                outdata = []
        #print outdata
        return serve_template("status.mako", title="Stats",inpss=stats)
        
class quickStatusPage:
    @cherrypy.expose
    def index(self):
        input = {}
        outdata = []
        p = {}
        parconn = {}
        chiconn = {}
        for data in sorted(bot.config["Servers"]):
            parconn[data], chiconn[data] = Pipe()
            p[data] = Process(target=dataget, args=(chiconn[data],hashedauth,bot,data,input))
            p[data].start()
        for data in sorted(bot.config["Servers"]):
            input[data] = parconn[data].recv()
            p[data].join()
        cluster = 0
        clusters = 0
        stats = []
        for inpdata in sorted(input):
            cluster+=1
            if type(input[inpdata])==type({}):
                outdata.append("<h2>"+inpdata+'    <span class="label label-success">Online</span></h2>\n')
            else:
                if (str(input[inpdata])=="[Errno 111] Connection refused"):
                    outdata.append("<h2>"+inpdata+'    <span class="label label-success">Online<span class="label label-important"><span title="The Server is Online but the ServPanel Client is not running or the ServPanel Client is not running on the port defined in the config."><b>!!</b></span></span></span></h2>')
                else:
                    outdata.append("<h2>"+inpdata+'    <span class="label label-failure">Offline</span></h2>')
            if cluster==(len(bot.config["Servers"])/3):
                cluster = 0
                clusters += clusters
                if clusters==len(bot.config["Servers"]):
                    outdata[len(outdata)-1] = outdata[len(outdata)-1]+'</div>\n'
                else:
                    outdata[len(outdata)-1] = outdata[len(outdata)-1]+'</div>        <div class="span4">'
                for cludata in xrange(0,len(outdata)):
                    stats.append(outdata[cludata])
                outdata = []
        #print outdata
        return serve_template("status.mako", title="Stats",inpss=stats)
        
class WebInterface:
    """ main web interface class """
    status = StatusPage()
    quick = quickStatusPage()
    @cherrypy.expose
    def index(self):
        #input = client("127.0.0.1",4329,"requesting bot variable data " \
        #"refreshment. please respond.")
        return serve_template("index.mako", title="ServPanel", version=bot.ver)
        

def web_init(inputs=None,bots=None):
    print "Initalising web server..."
    global input
    input = {}
    global bot
    bot = bots
    hashauth = {}
    for data in sorted(bot.config["Servers"]):
        hashauth[data] = hashlib.sha512(hashlib.sha512(bot.config["Servers"][data]["user"]).hexdigest()+hashlib.sha512(bot.config["Servers"][data]["pass"]).hexdigest()).hexdigest()
    global hashedauth
    hashedauth = hashauth
    global_conf = {
        'global': { 'engine.autoreload.on': False,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'log.error_file': 'site.log',
        'log.screen': False
    }}
    application_conf = {
        '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir,
        'static'),
        }
    }
    cherrypy.config.update(global_conf)
    web_interface = WebInterface()
    print("Web server started")
    cherrypy.quickstart(web_interface, '/', config = application_conf)