"""
Modulo encargado de la toma de argumentos por linea de comandos
por parte del cliente
"""
import argparse as ap


_parser = ap.ArgumentParser()

_parser.add_argument("url", type=str,
                     nargs="+",
                     help="destintation to scrap")
_parser.add_argument("-t", "--tags", type=str,
                     nargs="+",
                     help="HTML tags to look for")
_parser.add_argument("-c", "--htmlclass", type=str,
                     nargs="+", default=[None],
                     help="HTML classes to look for")
_parser.add_argument("-s", "--style", type=str,
                     nargs="+", default=[None],
                     help="inline styles to look for")
_parser.add_argument("-a", "--address", type=str,
                     help="IP address of the server",
                     default="localhost")
_parser.add_argument("-p", "--port", type=int,
                     help="Server port",
                     default=9000)
_parser.add_argument("--separator", type=str,
                     help="Separate text by some char (,|.|:|;|...)",
                     default=" ")
_parser.add_argument("-o", "--outputfile", type=str,
                     help="file destinated to save the program output",
                     default="scrap.json")
_parser.add_argument("--dataonly",
                     help="Saves only the data field",
                     default=False, action="store_true")

_args = _parser.parse_args()


URL: list = _args.url
TAGS: list = _args.tags
CLASSES: list = _args.htmlclass
STYLES: list = _args.style
SERVER_IP: str = _args.address
SERVER_PORT: int = _args.port
SEPARATOR: str = _args.separator
OUTPUTFILE: str = _args.outputfile
DATAONLY: bool = _args.dataonly
