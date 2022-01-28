import re
from requests import (
    get
)
from bs4 import (
    BeautifulSoup
)


def get_parsed_website(url: str) -> BeautifulSoup:
    """
    Obtiene y parsea el sitio web pasado por parametos de la
    funcion. Retorna objeto BeautifulSoup.
    """
    response = get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    return soup


def search_data(soup: BeautifulSoup, tag: str, classes: str = None,
                styles: str = None, other: dict = {}):
    """
    Busca dentro del HTML parseado en un objeto BeautifulSoup le contenido
    que cumpla con los parametros de busqueda recibidos por parametros
    de la funcion. Retorna ...
    """
    attrs = {
        **other,
    }
    if classes is not None:
        attrs["classes"] = re.compile(classes + r".*")
    if styles is not None:
        attrs["styles"] = re.compile(styles + r".*")

    result = soup.find_all(tag, attrs=attrs)
    return result


def extract_text(result: list, separator: str = " ") -> list[str]:
    """
    Dado un set de elementos que cumplen los parametros de busqueda, se
    extraera el texto contenido dentro de cada elemento del conjunto,
    por mas que este sea un elemento compuesto por multiples tags con
    diferentes textos dentro.
    """
    return [spider(tag, separator) for tag in result]


def spider(obj, separator: str):
    """
    Dado un objeto que representa una estrucuta de etiquetas HTML, en
    caso de que posea texto como unico hijo, este retornara el mismo.
    En caso de que posea subestructuras por debajo de el, se navegara
    de forma recursiva hasta llegar a las hojas del arbol y asi retornar
    el texto de las mismas.
    """
    if obj.string is None:
        aux = ""
        for h in obj.children:
            aux += spider(h, separator) + separator
    else:
        aux = obj.string
    return aux


if __name__ == "__main__":
    b = get_parsed_website("https://openbenchmarking.org/test/pts/aircrack-ng")
    r = search_data(b, "div", ["div_table_row"], [" color: #f1052d;"])
    s = extract_text(r, ":")
    for i in s:
        print(i)