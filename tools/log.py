"""
Herramienta destina a visualizar la informacion de LOG
almacenada en la DB.
"""
from pymongo import (
    MongoClient
)
from tabulate import (
    tabulate
)
from csv import (
    writer
)


class LogVisor:
    def __init__(self, url) -> None:
        self.url = url
        self.mongoclient = MongoClient(url)
        self.db = self.mongoclient["scrappinghistorydb"]
        self.collection = self.db["history"]

    def see_log(self) -> None:
        # [print(doc) for doc in self.collection.find()]

        docs: list[dict] = self.collection.find()

        # Sacar los headers del primer elemento
        headers: list = list(docs[0].keys())

        # Obtener filas para tabla
        values: list[list] = [list(doc.values()) for doc in docs]

        table: tabulate = tabulate(
            values,
            headers=headers,
            tablefmt="fancy_grid"
        )

        self.log = [headers, *values]

        print(table)

    def save_log(self) -> None:
        with open("log.csv", "w+", newline="") as f:
            w = writer(f)
            w.writerows(self.log)
            f.close()


if __name__ == "__main__":
    import argparse as ap

    parser = ap.ArgumentParser()
    parser.add_argument(
        "-d", "--dburl", type=str,
        default="mongodb://localhost:27017/"
    )
    args = parser.parse_args()

    DBURL: str = args.dburl

    logvisor = LogVisor(
        DBURL,
    )
    logvisor.see_log()
    logvisor.save_log()
    exit(0)
