from request import parse_request
from config import config
import os

import loader

try:
    Loader = {'static': loader.StaticLoader,
              'wsgi': loader.WsgiLoader
             }[config['LOAD']]
except KeyError:
    Loader = loader.DummyLoader


from response import Response


class Client:
    def __init__(self, socket, _):
         self.socket = socket
         self._errors = []


    def get_request(self):
        self.request = self.socket.recv(1024).decode()
        return self.request


    def handle_request(self):
        BASE_DIR = config['HOME_DIR']
        # If it's static, we can just route it, otherwise load that onto the framework

        request = parse_request(self.request)

        if '400' in request:
            self.send(Response(400, "Bad Request"))
            return

        try:
            if request['route'] == "/favicon.ico":
                icon = open(f"{BASE_DIR}/favicon.ico", "rb").read()
                response = Response(200, icon, "image/gif")
                self.send(response)
            else:
                l = Loader(request)
                response = Response(l.status, l.data)
        except FileNotFoundError:
            if os.path.isfile(f"{BASE_DIR}/404.html"):
                data = open(f"{BASE_DIR}/404.html").read()
            else:
                data = open("/etc/mercury/html/404.html").read()
            response = Response(404, data)


    def send(self, response):
        response = response.serialize()
        self.socket.send(response)


    def log(self, logfiles):
        """
        Log request and errors
        """

        if self._errors:
            "Write to error log"


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self.socket.close()
