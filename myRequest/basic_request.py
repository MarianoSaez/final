from socket import (
    gethostbyname,
    socket,
    AF_INET,
    SOCK_STREAM,
)

from custom_errors import NoHostEspecifiedException


class BasicRequest(object):
    def __init__(self, port : int = 80, method: str = "GET", path: str = "/", headers: dict = {}, body: dict | str = None) -> None:
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.port = port
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    @property
    def headers(self) -> dict:
        return self.__headers

    @headers.setter
    def headers(self, value: dict) -> None:
        if ("Host" or "host") not in value:
            raise NoHostEspecifiedException


        if ("User-Agent" or "user-agent") not in value:
            value["User-Agent"] = "Mozilla/5.0" # Bastante estandar entre los scrappers
        
        self.__headers = value

        ip_addr = gethostbyname(self.headers["Host"])
        self.sock.connect((ip_addr, self.port))


    # Construye el request HTTP basico que sera enviado como texto plano
    # o encriptado por TLS segun el protocolo.
    # Retorna str : Cuerpo de la peticion HTTP/HTTPS
    def prepare_request(self) -> str:
        initial_req_line = f"{self.method} {self.path} HTTP/1.1\r\n"
        header_lines = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])

        r = initial_req_line + header_lines + "\r\n\r\n"

        if self.body is not None:
            r += self.body + "\r\n"

        return r

    
    # Las clases que implementen esta clase abstracta [BasicRequest]
    # deberan sobreescribir el metodo send_request segun su implementacion
    # lo determine.
    def send_request(self) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    req = BasicRequest(headers={"Host" : "um.edu.ar"}, body="Hola mundo!")
    req.prepare_request()
