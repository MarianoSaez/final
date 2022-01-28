#! /usr/bin/python
from CLI_managment import (
    URL,
    TAGS,
    CLASSES,
    STYLES,
    SERVER_IP,
    SERVER_PORT,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
)
# from ssl import (
#     create_default_context,
# )
from json import (
    dumps
)


def create_socket() -> socket:
    sock = socket(AF_INET, SOCK_STREAM)
    # TODO: Secure Socket Layer implementation
    # ctxt = create_default_context()
    # ctxt.load_default_certs()
    # sec_sock = ctxt.wrap_socket(sock)
    sock.connect((SERVER_IP, SERVER_PORT))
    return sock


if __name__ == "__main__":
    s = create_socket()
    data = {
        "urls": URL,
        "tags": TAGS,
        "classes": CLASSES,
        "styles": STYLES,
    }
    s.send(bytes(dumps(data), 'utf-8'))
    s.close()
    exit(0)
