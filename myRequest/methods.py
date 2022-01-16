from request import HTTPRequest, HTTPSRequest


__all__ = [
    get,
]

def get(url : str, ):
    """
    Determinar el HOST, PATH y Protocolo
    """
    return HTTPSRequest("GET", )