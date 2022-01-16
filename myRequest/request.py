from socket import (
    AF_INET,
    SOCK_STREAM,
    socket
    )
from ssl import (
    create_default_context,
)
from basic_request import BasicRequest


class HTTPRequest(BasicRequest):
    def __init__(self, port: int = 80, method: str = "GET", path: str = "/", headers: dict = ..., body: dict | str = None) -> None:
        super().__init__(port, method, path, headers, body)

    def send_request(self) -> None:
        r = self.prepare_request()
        self.sock.send(r.encode())

        while (1):
            data = self.sock.recv(2048)
            if len(data) < 1:
                break
            print(data.decode(errors='ignore'))


class HTTPSRequest(BasicRequest):
    def __init__(self, port: int = 443, method: str = "GET", path: str = "/", headers: dict = ..., body: dict | str = None) -> None:
        super().__init__(port, method, path, headers, body)

    def send_request(self) -> None:
        r = self.prepare_request()

        # Preparacion adicional del socket
        context = create_default_context()
        self.sock = context.wrap_socket(self.sock, server_hostname=self.headers["Host"])    # Reemplazar al socket anterior por uno con TLS

        self.sock.send(r.encode())

        while (1):
            data = self.sock.recv(2048)
            if len(data) < 1:
                break
            print(data.decode(errors='ignore'))



if __name__ == "__main__":

    try:
        req = HTTPRequest(headers={"Host" : "www.facebook.com"})
        req.send_request()
    except KeyboardInterrupt:
        sec_req = HTTPSRequest(headers={"Host" : "www.facebook.com"})
        sec_req.send_request()
