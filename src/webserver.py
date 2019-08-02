# a simple webserver
# written by Jake Masters

import socket
from handlers import *

host = '0.0.0.0'
port = 8000 # map to machine port 80 of docker container with `docker run -d -p 80:8000`

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(1)

def main():
    while True:
        client_connection, client_address = server_socket.accept()

        request = client_connection.recv(1024).decode()
        headers = request.split('\n')
        if headers[0] == "": # ignore empty requests
            continue
        url = headers[0].split(' ')[1]
        path = url.split('&')[0]
        arg_list = []
        for header in headers:
            if "Cookie:" in header:
                header = header.split(':')[1]
                cookies = header.strip(' \r\n').split(';')
                for cookie in cookies:
                    cookie = cookie.strip(' \r\n')
                    arg_list.append(cookie)

        # route-based mappings
        if path == "/":
            resource = "index.html"
            type = "html"
        elif path == "/test" or path == "/test/":
            resource = "test.html"
            type = "html"
        # insert more routes here
        else: # a specific file is being requested
            resource = path[1:]
            type = resource.split('.')[-1]
        
        # file-based mappings
        if type == "html":
            html_handler(client_connection, resource, arg_list)
        elif type == "png":
            png_handler(client_connection, resource)
        elif type == "ico":
            ico_handler(client_connection, resource)
        # call out to other handlers here
        else:
            not_found_handler(client_connection, resource)

    server_socket.close()
    return

main()