from CLI_management import (
    SERVER_PORT,
)

from subclasses import WebScrapperServer


if __name__ == "__main__":
    # s = socket(AF_INET, SOCK_STREAM)
    # s.bind(("0.0.0.0", SERVER_PORT))
    # s.listen()
    # conn, addr = s.accept()
    # data = conn.recv(2048)
    # params = loads(str(data, 'utf-8'))

    # print(params)

    # # TODO : Implementar multiprocesamiento
    # soup = get_parsed_website(params["urls"][0])
    # found = search_data(soup, params["tags"][0], params["classes"][0],
    #                     params["styles"][0])
    # col = extract_text(found)

    # for row in col:
    #     print(row)

    s = WebScrapperServer(SERVER_PORT)
    s.serve()
