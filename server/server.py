#!/usr/bin/env python
import os
import sys
import time
import socket
import ast
import json
import urllib2
from core import web

print("Starting ServPanel")
sys.path += ['plugins']
sys.path += ['core']
sys.path += ['lib']
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

if not os.path.exists(bot.logs_dir):
    os.mkdir(bot.logs_dir)
print("Starting ServPanel Server Ver: "+bot.ver)

def get(*args, **kwargs):
    return opens(*args, **kwargs).read()

def opens(url, query_params=None, user_agent=None, post_data=None,
         get_method=None, cookies=False, **kwargs):
    request = urllib2.Request(url, post_data)
    opener = urllib2.build_opener()
    return opener.open(request)

bot.term=False
bot.event={}
bot.event["startweb"] = True
    
web.web_init(input,bot)
