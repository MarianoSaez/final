"""
Modulo encargado de la toma de argumentos por linea de comandos
por parte del servidor
"""
import argparse as ap


_parser = ap.ArgumentParser()

_parser.add_argument("-p", "--port", type=int,
                     help="Server port",
                     default=9000)

_args = _parser.parse_args()


SERVER_PORT: int = _args.port
