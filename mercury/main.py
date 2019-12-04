import socket
import json
from client import Client
import os

from config import config


# Open socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((config['HOST'], int(config['PORT'])))
server_socket.listen()


logfiles = ['access_log', 'error_log']


while True:
    c_sock, addr = server_socket.accept()

    with Client(c_sock, addr) as client:
        try:
            client.get_request()
            client.handle_request()
            client.log(logfiles)
        except BrokenPipeError:
            print("Broken Pipe Error... ffs.")
