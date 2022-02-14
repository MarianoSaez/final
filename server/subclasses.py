from multiprocessing import (
    Process,
)
import os
# from concurrent.futures import (
#     ProcessPoolExecutor,
# )
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
from task_queue.scrap_tasks import (
    scrap,
)
from pymongo import (
    MongoClient,
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
            """
            Funcion manejadora de interrupciones. Disparada por SIGINT.
            Espera y libera los recursos utilizados por el servidor.
            """
            print("\nCerrando servidor")
            for proc in proc_list:
                proc.join()
            s.close()
            exit(0)

        signal(SIGINT, handler)

        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("0.0.0.0", self.port))
        s.listen()

        proc_list: list[Scrapper] = list()

        while True:
            conn, addr = s.accept()     # Bloquea hasta recibir otra conexion
            print(f"Nueva conexion desde {addr[0]}:{addr[1]}")

            scrapper = Scrapper(conn)
            proc_list.append(scrapper)  # En caso de tener que esperarlos
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
        args: list[tuple] = list()
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

        """
        Reemplzado por Cola de Tareas en Celery

        with ProcessPoolExecutor() as browsers:
            # result = browsers.map(scrap, args, chunksize=10)
            future_result = [browsers.submit(scrap, arg) for arg in args]
        """

        # Lanzar a la cola de tareas
        future_result = [scrap.delay(arg) for arg in args]

        # Pasar de objeto futuro a lista
        result = [r.get() for r in future_result]

        # Reconvertir el campo data a un objeto de python
        for i in result:
            i["data"] = loads(i["data"])

        # Devolver al cliente el resultado de la busqueda
        self.send_data(result)

        # Por ultimo. Guardar log en la DB.
        self.log_scrap(result)

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

    def send_data(self, result: list) -> None:
        """
        Realizar el envio de la informacion obtenida del proceso de scrapping.
        """
        BUFFSIZE = 4096

        data = dumps(result, indent=4)
        raw = data.encode('utf-8')

        # Linea complicada - Evita iterar mas de una vez
        [self.conn.send(raw[i:i+BUFFSIZE])
            for i in range(0, len(raw), BUFFSIZE)]

        """
        Equivalente:

        for i in range(0, len(raw), BUFFSIZE):
            aux = raw[i:i+BUFFSIZE]
            self.conn.send(aux)

        """

    def log_scrap(self, result: list[dict]) -> None:
        client = MongoClient(os.environ.get("MONGODB_URL"))
        db = client["scrappinghistorydb"]
        history = db["history"]

        for r in result:
            del r["data"]   # Remover datos de la busqueda para ahorrar espacio

        history.insert_many(result)     # Insertar "cabeceras" en la DB


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
