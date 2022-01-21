class NoHostEspecifiedException(Exception):
    """
    Error levantado cuando no se especifico ningun
    host al cual direccionar el Request
    """

class BadUrlProvidedException(Exception):
    """
    Error levantado cuando las expresiones regulares
    usadas para determinar protocolo, host y path
    levantaron AttributeError
    """