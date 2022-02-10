from datetime import (
    datetime
)
from json import dumps
from os import (
    getpid
)
import re
from time import (
    time
)
from requests import (
    get,
    exceptions,
)
from bs4 import (
    BeautifulSoup
)
from .custom_errors import (
    PageNotFound,
    CouldNotScrape,
    EmptyScrapeList,
)
from .celery import (
    app
)


def get_parsed_website(url: str) -> tuple[BeautifulSoup, int, str]:
    """
    Obtiene y parsea el sitio web pasado por parametos de la
    funcion. Retorna objeto BeautifulSoup.
    """
    try:
        response = get(url)
        code = response.status_code
        response.raise_for_status()     # Levantar request.exceptions.HTTPError
        err = None

    except exceptions.HTTPError:
        if code < 500:
            err: Exception = PageNotFound(url)
        else:
            err: Exception = CouldNotScrape(url, code)
        raise err

    finally:
        soup = BeautifulSoup(response.content, features="html.parser")
        return soup, code, str(err)


def search_data(soup: BeautifulSoup, tag: str, classes: list = None,
                styles: list = None, other: dict = {}):
    """
    Busca dentro del HTML parseado en un objeto BeautifulSoup le contenido
    que cumpla con los parametros de busqueda recibidos por parametros
    de la funcion. Retorna ...
    """
    attrs = {
        **other,
    }
    if classes is not None:
        attrs["class"] = re.compile(" ".join(classes) + r".*")
    if styles is not None:
        attrs["style"] = re.compile(" ".join(styles) + r".*")

    result = soup.find_all(tag, attrs=attrs)
    return result


def extract_text(result: list) -> tuple[list[str], str]:
    """
    Dado un set de elementos que cumplen los parametros de busqueda, se
    extraera el texto contenido dentro de cada elemento del conjunto,
    por mas que este sea un elemento compuesto por multiples tags con
    diferentes textos dentro.
    """
    err = None
    text_list = list()

    for tag in result:
        aux = list()
        spider(tag, aux)
        text_list.append(aux)

    if len(text_list) == 0:
        err = EmptyScrapeList()

    return text_list, str(err)


def spider(obj, m: list = []):
    """
    Funcion recursiva. Recorre el arbol de HTML hasta sus hojas
    devolviendo el texto, contenido en las mismas, agregandolo a
    una lista pasada por refencia.
    """
    if obj.string is None:
        for h in obj.children:
            spider(h, m)
    else:
        m.append(obj.string)


@app.task
def scrap(args: tuple) -> dict:
    """
    Wrapper del procedimiento de scrapping. Utilizado para ser pasado como
    identificador de funcion a procesos que deban realizar las tres acciones
    principales, mediante una unica llamada a funcion. Retorna lista de strings
    """
    start = time()

    url = args[0]
    tag, classes, styles, other = args[1:5]
    # separator = args[-1]  # Futuras implementaciones del separador

    soup, code, web_err = get_parsed_website(url)
    result = search_data(soup, tag, classes, styles, other)
    string_list, list_err = extract_text(result)

    final = {
        "pid": getpid(),
        "date": str(datetime.now()),
        "time_elapsed": time() - start,
        "url": url,
        "code": code,
        "errors": [
            web_err,
            list_err,
        ],
        "search_params": {
            "tag": tag,
            "classes": classes,
            "styles": styles,
        },
        "record_number": len(string_list),
        "data": dumps(string_list),
    }

    return final


# Para pruebas unicamente
if __name__ == "__main__":
    # b=get_parsed_website("https://openbenchmarking.org/test/pts/aircrack-ng")
    # r = search_data(b, "div", "div_table_row", " color: #f1052d;")
    # s = extract_text(r, ":")
    # for i in s:
    #     print(i)

    args: tuple = (
        "https://openbenchmarking.org/test/pts/aircrack-ng",
        "div",
        ["div_table_row"],
        ["color: #"],
        {},
        "#",
    )
    data: list = scrap(args)["data"]
    [print(i) for i in data]
