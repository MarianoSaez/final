from multiprocessing import (
    Process,
)
from concurrent.futures import (
    ProcessPoolExecutor,
)
from scrapping_functions import (
    scrap,
)
from socket import (
    socket,
    AF_INET,
    SOCK_STREAM,
)
from json import (
    dumps,
    loads,
)
from signal import (
    signal,
    SIGINT
)


class WebScrapperServer():
    """
    Clase encargada de actuar como servidor de conexiones. Crean un proceso
    scrapper que se encarga de atender la conexion.
    """
    def __init__(self, port):
        self.port = port

    def serve(self):
        print("Inicializando servidor")

        def handler(signum, frame):
            print("\nCerrando servidor")
            s.close()
            exit(0)

        signal(SIGINT, handler)

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("0.0.0.0", self.port))
        s.listen()

        while True:
            conn, addr = s.accept()     # Bloquea hasta recibir otra conexion
            print(f"Nueva conexion desde {addr[0]}:{addr[1]}")

            scrapper = Scrapper(conn)
            scrapper.start()


class Scrapper(Process):
    """
    Esta clase es la encargada de atender la conexiones y desplegar los
    buscadores para obtener la informacion buscada.
    """
    def __init__(self, conn: socket,
                 urls: list = [], tags: list = [],
                 classes: list = [], styles: list = [],
                 separator: str = " ", **kwargs):
        super(Scrapper, self).__init__()
        self.conn = conn
        self.urls = urls
        self.tags = tags
        self.classes = classes
        self.styles = styles
        self.separator = separator
        self.own_kwargs = kwargs

        # TODO : Implementacion de futuros atributos

    def run(self):
        """
        Realizar busqueda y procesamiento de las paginas
        """
        self.recv_conn()
        args = list()
        for i in range(len(self.urls)):
            arg_tuple = (
                self.urls[i],
                self.tags,
                self.classes,
                self.styles,
                {},  # Para futuras implementaciones de kwargs
                self.separator,
            )
            args.append(arg_tuple)

        with ProcessPoolExecutor() as browsers:
            result = browsers.map(scrap, args)
            browsers.shutdown(wait=True)

        # Devolver al cliente el resultado de la busqueda
        # for i in result:
        #     print("".center(80, "="))
        #     for j in i:
        #         print(f"{j} : {i[j]}")

        data = dumps(list(result), indent=4)
        raw = data.encode('utf-8')
        self.conn.send(raw)

    def recv_conn(self) -> None:
        """
        Setup del proceso con la informacion necesaria, recibida via socket
        para realizar las busquedas.
        """
        raw = self.conn.recv(4096)
        params = loads(raw.decode('utf-8'))

        self.urls = params["urls"]
        self.tags = params["tags"]
        self.classes = params["classes"]
        self.styles = params["styles"]
        self.separator = params["separator"]
        # self.own_kwargs = params["kwargs"]


if __name__ == "__main__":
    urls = [
        "https://openbenchmarking.org/test/pts/aircrack-ng",
        "https://openbenchmarking.org/test/pts/compress-7zip-1.8.0",
        "https://openbenchmarking.org/test/pts/aom-av1-3.2.0",
    ]
    tags = "div"
    classes = "div_table_row"
    styles = " color: #f1052d;"
    s = Scrapper(urls, tags, classes, styles)
    s.start()
    s.join()
    exit(0)
