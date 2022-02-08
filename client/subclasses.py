from json import (
    dumps,
    loads,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
)
from custom_errors import (
    ServerNotFound,
)
from csv import (
    writer,
)
"""
TODO:
    - Implementacion de SSL para la conexion cliente-servidor
    - Agregado de funcionalidades adicionales, como guardado en formato csv
"""

ENCODING = "utf-8"


class WebScrapperClient():
    """
    Clase encargada de todas las funcionalidades respectivas del
    cliente del WebScrapperServer.
    """

    def __init__(self, server_addr: tuple, data: dict, sep: str,
                 dataonly: bool = False,
                 outputfile: str = "scrap.json") -> None:
        self.server_addr = server_addr
        self.data = data
        self.sep = sep
        self.dataonly = dataonly
        self.outputfile = outputfile

    def create_socket(self) -> None:
        """
        Crear socket TCP
        """
        self.sock = socket(AF_INET, SOCK_STREAM)
        try:
            # TODO: Secure Socket Layer implementation
            # ctxt = create_default_context()
            # ctxt.load_default_certs()
            # sec_sock = ctxt.wrap_socket(sock)
            self.sock.connect(self.server_addr)
        except ConnectionRefusedError:
            raise ServerNotFound(*self.server_addr)

    def prepare_data_to_send(self) -> None:
        """
        Preparar datos para el envio. Pasar a string y codificarlo.
        """
        self.sendable = dumps(self.data).encode(ENCODING)

    def save_scrapped(self) -> None:
        """
        Almacenar el resultado de la busqueda
        """
        parsed: list[dict] = loads(self.raw_response)

        if self.dataonly:
            self.saved = dumps([field["data"] for field in parsed], indent=4)
        else:
            self.saved = self.raw_response

        file = CSV(self.outputfile.strip(".json") + ".csv", parsed, self.sep)
        file.save()

        with open(self.outputfile, "w") as out:
            out.write(self.saved)
            out.close()

    def close_client(self) -> None:
        """
        Procedimiento para liberar recursos utlizados por la instancia
        de cliente.
        """
        self.sock.close()

    def main(self) -> None:
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


class File:
    """
    Clase abtracta. Los diferentes formatos de archivos implementan
    sus metodos de la manera apropiada segun correponda.
    """
    def __init__(self, name: str, data: list[dict], sep: str) -> None:
        self.name = name
        self.sep = sep
        self.data = data

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list[dict]) -> None:
        s: list[list[str]] = [field["data"] for field in value]
        aux = list()
        for i in s:
            for j in i:
                aux.append(j.split(self.sep))
        self.__data: list[str] = aux

    def save(self) -> None:
        raise NotImplementedError


class CSV(File):
    def __init__(self, name: str, data: list[dict], sep: str) -> None:
        super().__init__(name, data, sep)

    def save(self) -> None:
        """
        Guardar en formato csv la informacion recibida
        """
        with open(self.name, "w+", newline="") as f:
            w = writer(f)
            w.writerows(self.data)
