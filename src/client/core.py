import socket
import threading


class ClientSocket:
    def __init__(self) -> None:
        self._connected: bool = False

    def connect(self, ip: str = "localhost", port: int = 8080) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            self._connected = True
            recv_thread = threading.Thread(
                target=self._receive, args=(sock,), daemon=True
            )
            recv_thread.start()

    def _receive(self, sock: socket.socket) -> None:
        while self._connected:
            try:
                data = sock.recv(1024)
                if not data:
                    self._disconnect()
                else:
                    print(data.decode())
            except ConnectionResetError:
                self._disconnect()

    def _send(self, sock: socket.socket, msg: bytes) -> None:
        sock.send(msg)

    def _disconnect(self) -> None:
        self._connected = False
