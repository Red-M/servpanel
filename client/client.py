#!/usr/bin/env python
from datetime import timedelta
import os
import time
import socket
import platform
import ast
import json
import urllib2
import struct
import threading
import SocketServer
import hashlib
import sys
import psutil

print("Starting ServPanel")
sys.path += ['core']
os.chdir(sys.path[0] or '.')
class Bot(object):
    pass
bot = Bot()
eval(compile(open(os.path.join('core', 'reload.py'), 'U').read(),
    os.path.join('core', 'reload.py'), 'exec'))
reload(init=True)

print("Loading config.")
config()
if not hasattr(bot, 'config'):
    print("First time run or no config found.")
    exit()
print("Done loading rules.")

bot.ver="1.00"
bot.path=__file__
bot.abspath=(os.path.abspath(bot.path).replace(bot.path.replace("./",""),""))+"/"
bot.logs_dir = os.path.abspath('logs')

bot.start_time = time.time()

if not os.path.exists(bot.logs_dir):
    os.mkdir(bot.logs_dir)
print("Starting ServPanel Client Ver: "+bot.ver)

def get(*args, **kwargs):
    return opens(*args, **kwargs).read()

def opens(url, query_params=None, user_agent=None, post_data=None,
         get_method=None, cookies=False, **kwargs):
    request = urllib2.Request(url, post_data)
    opener = urllib2.build_opener()
    return opener.open(request)

bot.term=False

def savevars(bot,input):
    test={}
    test['Python version'] = sysinfo["pyver"]
    test['CPU'] = cpuinfo(input)
    test['CPU cores'] = cpu_cores(input)
    test['Host'] = platform.node()
    test['OS'] = platform.platform()
    test['Bit'] = '-'.join(platform.architecture())
    test['Uptime'] = uptime(bot)
    test['RAM'] = vmem(input)
    test['SWAP'] = virtmem(input)
    test['Disk'] = dmem(input)
    return test
    
def uptime(bot):
    uptime_raw = round(time.time() - psutil.BOOT_TIME)
    uptime = timedelta(seconds=uptime_raw)
    return "Uptime: %s" % uptime

def vmem(input):
    return(sysinfo["ram"])
    
def virtmem(input):
    return(sysinfo["swap"])
    
def dmem(input):
    total, used, free, percent = psutil.disk_usage('/')
    diskdata = str(total)+" "+str(used)+" "+str(free)+" "+str(percent)
    return(diskdata)
    
def cpuinfo(input):
    return(str(psutil.cpu_times()))
    
def cpu_cores(input):
    return(str(psutil.NUM_CPUS))

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        sent = False
        data = self.request.recv(1024)
        #print(auth)
        if data==auth:
            self.request.sendall(str(savevars(bot,input)))
            #print("matched")
            sent = True
        if data=="bot term. shutdown. NOW":
            self.server.shutdown()
            #os._exit(0)
            sent = True
    
    
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

server_thread = threading.Thread(target=ThreadedTCPServer((bot.config["ip"], int(bot.config["port"])),ThreadedTCPRequestHandler).serve_forever)
server_thread.daemon = True
server_thread.start()
global sysinfo
sysinfo = {}
sysinfo["ram"] = str(psutil.TOTAL_PHYMEM/1024/1024)
sysinfo["swap"] = str(psutil.total_virtmem()/1024/1024)
sysinfo["pyver"] = ('%s %s' %
                (platform.python_implementation(),platform.python_version()))
global auth
auth = hashlib.sha512(hashlib.sha512(bot.config["user"]).hexdigest()+hashlib.sha512(bot.config["pass"]).hexdigest()).hexdigest()

while True:

    time.sleep(2)
