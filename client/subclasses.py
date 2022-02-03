from json import (
    dumps,
    loads,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
)

ENCODING = "utf-8"


class WebScrapperClient():
    """
    Clase encargada de todas las funcionalidades respectivas del
    cliente del WebScrapperServer.
    """

    def __init__(self, server_addr: tuple, dataonly: bool = False,
                 outputfile: str = "scrap.json") -> None:
        self.server_addr = server_addr
        self.dataonly = dataonly
        self.outputfile = outputfile

    def create_socket(self) -> None:
        """
        Crear socket TCP
        """
        self.sock = socket(AF_INET, SOCK_STREAM)
        # TODO: Secure Socket Layer implementation
        # ctxt = create_default_context()
        # ctxt.load_default_certs()
        # sec_sock = ctxt.wrap_socket(sock)
        self.sock.connect(self.server_addr)

    def prepare_data_to_send(self) -> None:
        """
        Preparar datos para el envio. Pasar a string y codificarlo.
        """
        self.sendable = dumps(self.data).encode(ENCODING)

    def save_scrapped(self) -> None:
        """
        Almacenar el resultado de la busqueda
        """
        if self.dataonly:
            parsed: list[dict] = loads(self.raw_response)
            self.saved = dumps([field["data"] for field in parsed], indent=4)
        else:
            self.saved = self.raw_response

        with open(self.outputfile, "w") as out:
            out.write(self.saved)
            out.close()

    def close_client(self) -> None:
        """
        Procedimiento para liberar recursos utlizados por la instancia
        de cliente.
        """
        self.sock.close()

    def main(self, data: dict, dataonly: bool, outputfile: str) -> None:
        """
        Funcion principal del cliente
        """
        # Crear socket
        self.create_socket()

        # Preparar datos para el envio del request
        self.prepare_data_to_send()
        self.sock.send(self.sendable)

        # Bloquearse hasta obtener respuesta del server
        self.raw_response = self.sock.recv(32768).decode()

        # Guardar en archivo la busqueda
        self.save_scrapped()

        # Cerrar cliente
        self.close_client()
