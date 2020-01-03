import json
import platform
import sys


with open('/etc/mercury/conf', 'r') as f:
    config = json.load(f)

if config['LOAD'] == 'wsgi':
    if "APP" not in config:
        print("Error: wsgi was enabled but no app was specified.")
        sys.exit()
elif config['LOAD'] == 'static':
    if "HOME_DIR" not in config:
        print("Error: static loading was enabled but no home directory was specified.")
        sys.exit()

config['SYSTEM'] = platform.system()
