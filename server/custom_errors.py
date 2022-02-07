"""
En este archivo se encuentran algunas de las excepciones que
pueden ser levantadas por el codigo servidor.
"""


class PageNotFound(Exception):
    """
    Excepcion levantada cuando la URL provista retorna un error
    404 NOT FOUND.
    """
    def __init__(self, url,
                 message="No se encontro la pagina solicitada") -> None:
        super().__init__(message)
        self.url = url
        self.message = message

    def __str__(self) -> str:
        return f"{self.message} : URL:{self.url}"


class CouldNotScrape(Exception):
    """
    Excepcion levantada en casos de sitios web que posean sistemas
    de prevencion de BOTS que bloquean la peticion de la herramienta.
    """
    def __init__(self, url: str, code: int = 999,
                 message="La pagina solicitada bloqueo la peticion del"
                 "la herramienta") -> None:
        super().__init__(message)
        self.message = message
        self.url = url
        self.code = code

    def __str__(self) -> str:
        return f"{self.message} : URL ({self.url}) returned {self.code} CODE"


class EmptyScrapeList(Exception):
    """
    Excepcion levantada cuando ningun hijo dentro del arbol de parseo generado
    BeautifulSoup coincide con los parametros recibidos.
    """
    def __init__(self, message="Ningun hijo en el arbol coincide con los"
                 "parametros de busqueda") -> None:
        super().__init__(message)
