import sys

from src.server import ServerApp
from src.client import ClientApp


def main():
    match sys.argv:
        case [*_, "--host"]:
            run_server()
        case _:
            run_client()


def run_server() -> None:
    server = ServerApp()
    server.run()


def run_client() -> None:
    client = ClientApp()
    client.run()


if __name__ == "__main__":
    main()
