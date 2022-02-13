#! /usr/bin/python
from CLI_managment import (
    DATAONLY,
    URL,
    TAGS,
    CLASSES,
    STYLES,
    SEPARATOR,
    OUTPUTFILE,
    SERVER_IP,
    SERVER_PORT,
    TIMEOUT,
    FILE,
    ALLTOGETHER,
)
from subclasses import WebScrapperClient


if __name__ == "__main__":

    DATA = {
        "urls": URL,
        "tags": TAGS,
        "classes": CLASSES,
        "styles": STYLES,
        "separator": SEPARATOR,
    }
    c = WebScrapperClient(
        (SERVER_IP, SERVER_PORT),
        DATA,
        SEPARATOR,
        TIMEOUT,
        FILE,
        DATAONLY,
        ALLTOGETHER,
        OUTPUTFILE
    )
    c.main()

    exit(0)
