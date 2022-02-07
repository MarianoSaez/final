from CLI_management import (
    SERVER_PORT,
)

from subclasses import WebScrapperServer


if __name__ == "__main__":

    s = WebScrapperServer(SERVER_PORT)
    s.serve()
