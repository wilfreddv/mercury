from request import parse_request
from config import config
from datetime import datetime
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
         self._log_data = ""


    def get_request(self):
        self.request = self.socket.recv(1024).decode()
        self._log_data += '"' + self.request.split('\n')[0].strip() + '"'
        return self.request


    def handle_request(self):
        BASE_DIR = config['HOME_DIR']
        # If it's static, we can just route it, otherwise load that onto the framework

        request = parse_request(self.request)

        if 'Accept' in request:
            mime = request['Accept'].split(',')[0]
        else:
            mime = "*/*"

        if '400' in request:
            self.send(Response(400, "Bad Request"))
            status_code = 400
            return

        try:
            if request['route'] == "/favicon.ico":
                icon = open(f"{BASE_DIR}/favicon.ico", "rb").read()
                response = Response(200, icon, "image/gif")
                self.send(response)
                status_code = 200
            else:
                l = Loader(request)
                response = Response(l.status, l.data, content_type=mime)
                status_code = l.status
        except FileNotFoundError:
            if os.path.isfile(f"{BASE_DIR}/404.html"):
                data = open(f"{BASE_DIR}/404.html").read()
            else:
                data = open("/etc/mercury/html/404.html").read()
            response = Response(404, data)
            status_code = 404

        self._log_data += f" {status_code}"
        self.send(response)


    def send(self, response):
        response = response.serialize()
        self.socket.send(response)


    def log(self, logfiles):
        """
        Log request and errors
        """
        now = datetime.now()
        timestamp = now.strftime("[ %d-%m-%Y - %H:%M:%S ]")

        with open(logfiles[0], 'a') as f:
            f.write(f"{timestamp} {self._log_data}\n")

        if self._errors:
            with open(logfiles[1], 'a') as f:
                for err in self._errors:
                    f.write(f"{timestamp} {err}\n")


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self.socket.close()
