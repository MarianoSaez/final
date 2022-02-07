"""
En este archivo se encuentran algunas de las excepciones que
pueden ser levantadas por el codigo cliente.
"""


class ServerNotFound(Exception):
    """
    Excepcion levantada para intentos fallidos de conexion
    con el WebScrappingServer
    """

    def __init__(self, addr: str, port: int,
                 message: str = "Servidor no fue encontrado en el destino"
                 " indicado") -> None:
        self.addr = addr
        self.port = port
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} : SERVER_ADDR={self.addr}:{self.port}"
