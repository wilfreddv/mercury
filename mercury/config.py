import json
import platform

with open('/etc/mercury/conf', 'r') as f:
    config = json.load(f)

config['SYSTEM'] = platform.system()
