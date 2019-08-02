# routing handlers
# a handler is responsible for:
#   - retrieving resources
#   - sending to client
# basically, once the handler runs, the connection cloess

from render import *

DATA_ROOT = "templates/"
STATIC_ROOT = "static/"

# a different approach
def html_handler(client_connection, resource, arg_list):
    template = DATA_ROOT + resource
    data = open(template)
    content = data.read()
    data.close()

    # render template
    content = render(content, arg_list)

    client_connection.send('HTTP/1.1 200 OK\n'.encode())
    client_connection.send('Content-type: text/html\n'.encode())
    # here is where any cookies would be set
    client_connection.send('Set-Cookie: foo=bar\n\n'.encode())
    client_connection.send(content.encode())
    client_connection.close()
    return

def png_handler(client_connection, resource):
    # under the guise that all static files are uniquely named and stored in one "static" directory...
    resource = resource.split('/')[-1]

    template = STATIC_ROOT + resource
    data = open(template, 'rb')
    content = data.read()
    data.close()

    client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
    client_connection.send("Content-Type: image/png\r\n".encode())
    client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode())
    client_connection.send(content)
    client_connection.close()
    return

def ico_handler(client_connection, resource):
    # under the guise that all static files are uniquely named and stored in one "static" directory...
    resource = resource.split('/')[-1]

    template = STATIC_ROOT + resource
    data = open(template, 'rb')
    content = data.read()
    data.close()

    client_connection.send('HTTP/1.1 200 OK\r\n'.encode())
    client_connection.send("Content-Type: image/ico\r\n".encode())
    client_connection.send("Accept-Ranges: bytes\r\n\r\n".encode())
    client_connection.send(content)
    client_connection.close()
    return

def not_found_handler(client_connection, resource):
    template = DATA_ROOT + "not_found.html"
    data = open(template)
    content = data.read()
    data.close()

    client_connection.send('HTTP/1.0 404 NOT FOUND\n\n'.encode())
    client_connection.send(content.encode())
    client_connection.close()
    return
