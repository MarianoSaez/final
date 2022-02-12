from json import (
    dumps,
    loads,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
    timeout as Timeout,
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
"""

ENCODING = "utf-8"
BUFFSIZE = 4096


class WebScrapperClient():
    """
    Clase encargada de todas las funcionalidades respectivas del
    cliente del WebScrapperServer.
    """

    def __init__(self, server_addr: tuple, data: dict, sep: str,
                 timeout: int, file: str,
                 dataonly: bool = False,
                 outputfile: str = "scrap.json") -> None:
        self.server_addr = server_addr
        self.data = data
        self.sep = sep
        self.dataonly = dataonly
        self.outputfile = outputfile
        self.timeout = timeout
        self.file = file

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, value: str) -> None:
        # Setear las urls desde el archivo
        if value:
            with open(value, "r") as f:
                urls: list = f.read().splitlines()
                self.data["urls"] = urls

        # Finalmente asignar valor al atributo
        self.__file = value

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

        # Respecto al json. Guardar o no info. de control.
        if not self.dataonly:
            with open(self.outputfile, "w") as out:
                out.write(self.raw_response)
                out.close()
        else:
            json_file = JSON(self.outputfile, parsed, self.sep)
            json_file.save()

        # Respecto al csv. Guardar.
        csv_file = CSV(self.outputfile, parsed, self.sep)
        csv_file.save()

    def close_client(self) -> None:
        """
        Procedimiento para liberar recursos utlizados por la instancia
        de cliente.
        """
        self.sock.close()

    def recv_data(self) -> None:
        """
        Procedimiento para recibir informacion desde el servidor.
        """
        self.sock.settimeout(self.timeout)     # Fijar timeout
        data = self.sock.recv(BUFFSIZE)
        while len(data) > 0:
            try:
                data += self.sock.recv(BUFFSIZE)
            except Timeout:       # Cachear excepcion de Timeout
                break
        self.raw_response = data.decode()

    def main(self) -> None:
        """
        Funcion principal del cliente
        """
        # Crear socket
        self.create_socket()

        # Preparar datos para el envio del request
        self.prepare_data_to_send()
        print(self.data["urls"])
        self.sock.send(self.sendable)

        # Bloquearse hasta obtener respuesta del server
        self.recv_data()

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
        self.__data = list()
        for i in s:
            for j in i:
                self.__data.append(j)

    def save(self) -> None:
        raise NotImplementedError


class CSV(File):
    def __init__(self, name: str, data: list[dict], sep: str) -> None:
        super().__init__(name, data, sep)

    def save(self) -> None:
        """
        Guardar en formato csv la informacion recibida
        """
        with open(self.name + ".csv", "w+", newline="") as f:
            w = writer(f)
            w.writerows(self.data)


class JSON(File):
    def __init__(self, name: str, data: list[dict], sep: str) -> None:
        super().__init__(name, data, sep)

    def save(self) -> None:
        """
        Guardar en formato JSON
        """
        with open(self.name + ".json", "w+") as f:
            j: str = dumps(self.data, indent=4)
            f.write(j)
