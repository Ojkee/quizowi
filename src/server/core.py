import socket
import logging

LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "CONNECTED - %(message)s"
LOG_FORMATTER = logging.Formatter(LOG_FORMAT)


class ServerSocket:
    HOST = "127.0.0.1"
    LOGGER.setLevel(logging.INFO)
    CONSOLE_LOG = logging.StreamHandler()
    CONSOLE_LOG.setFormatter(LOG_FORMATTER)
    LOGGER.addHandler(CONSOLE_LOG)

    def __init__(self, port: int, max_room: int = 6) -> None:
        self._port: int = port
        self._max_room: int = max_room
        self._conns: list[socket.socket] = []

    def run(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.HOST, self._port))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.listen(self._max_room)
            while True:
                connection, address = sock.accept()
                connection.send(f"Hello {address}".encode())
                self._conns.append(connection)
                LOGGER.info(str(address))
