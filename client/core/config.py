import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=1)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
r'''{
"user": "admin",
"pass": "test",
"port": 5555,
"ip": "127.0.0.1"
}
''') + '\n')

def config():
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError, e:
            print 'ERROR: malformed config!', e


bot._config_mtime = 0