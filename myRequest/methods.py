from custom_errors import BadUrlProvidedException
from request import HTTPRequest, HTTPSRequest
from re import (
    search,
)


URLPATTERN = r"(https)?(\:\/\/)?([^\/]+)(\/.*)"


def get(url : str):
    """
    Determinar el HOST, PATH y Protocolo
    """
    try:
        m = search(URLPATTERN, url)

        # Se determinan las partes necesarias para construir el
        # request HTTP/HTTPS
        
        host = m.group(3)
        path = m.group(4)

        if m.group(1) == "https":
            port = 443
            return HTTPSRequest(port, "GET", path, headers={"Host" : host}).send_request()
        else:
            port = 80
            return HTTPRequest(port, "GET", path, headers={"Host" : host})



    except AttributeError:
        raise BadUrlProvidedException

    
        

if __name__ == "__main__":
    get("https://www.amazon.com/")