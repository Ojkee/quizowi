import sys

from src.server import ServerApp


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
    pass


if __name__ == "__main__":
    main()
