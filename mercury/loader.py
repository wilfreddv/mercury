import os
from os.path import isfile, isdir
from pathlib import Path
from config import config
import jinja2


class StaticLoader:
    def __init__(self, request):
        BASE = config['HOME_DIR']
        
        route = request['route']
        path = f"{BASE}{route}"
        
        
        if request['route'] == "/favicon.ico":
            try:
                self.data = open(path, "rb").read()
                self.status = 200
            except FileNotFoundError:
                self.data = ""
                self.status = 404

        elif isdir(path):
            self.status = 200
            if isfile(f"{path}/index.html"):
                self.data = open(f"{path}/index.html", "r").read()
            else:
                self.data = self._build_dir_list(route, path)
        
        elif not isfile(path):
            self.status = 404
            if isfile(f"{BASE}/404.html"):
                f = f"{BASE}/404.html"
            else:
                f = "/etc/mercury/html/404.html"
            self.data = open(f, "r").read()
        
        else:
            self.status = 200
            self.data = open(path, "r").read()


    def _build_dir_list(self, route, path):
        _, dirs, files = next(os.walk(path))
        
        parent = '/'.join(route.split('/')[:-1]) or '/'
        template = open('/etc/mercury/html/_list_directory_template.html').read()
        template = jinja2.Template(template)
        data = template.render(route=route, dirs=sorted(dirs), files=sorted(files), parent=parent)
        return data


class WsgiLoader:
    def __init__(self, request):
        self.status = 200
        self.data = """"<h3>Should be generated using a WSGI app</h3>"""


class DummyLoader:
    def __init__(self, request):
        self.status = 200
        self.data = """<h3>Hello World!</h3>"""
