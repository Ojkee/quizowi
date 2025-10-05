import asyncio
import logging
import threading
from typing import Optional

from src.observers import EventBus, ClientConnected, ClientDisconnected

from .connected_client import ConnectedClient

LOGGER = logging.getLogger(__name__)
LOG_FORMAT = "INFO - %(message)s"
LOG_FORMATTER = logging.Formatter(LOG_FORMAT)


class ServerSocket:
    HOST = "127.0.0.1"
    LOGGER.setLevel(logging.INFO)
    CONSOLE_LOG = logging.StreamHandler()
    CONSOLE_LOG.setFormatter(LOG_FORMATTER)
    LOGGER.addHandler(CONSOLE_LOG)

    def __init__(self, event_bus: EventBus, port: int, max_room: int = 6) -> None:
        self._event_bus = event_bus
        self._port: int = port
        self._max_room: int = max_room

        self._loop = asyncio.new_event_loop()
        self._self_t = threading.Thread(target=self._run_loop, daemon=True)

        self._clients: set[ConnectedClient] = set()
        self._server: Optional[asyncio.Server] = None

    def start(self) -> None:
        LOGGER.info(f"Starting server at port: {self._port}")
        self._self_t.start()

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._start())

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        if len(self._clients) >= self._max_room:
            writer.close()
            await writer.wait_closed()
            return
        addr = writer.get_extra_info("peername")
        LOGGER.info(f"CONNECTED: {addr}")
        client = ConnectedClient(writer)

        # TODO: implement message for handling nicknames with discarding existing ones
        client.nick = f"TEST_NICK {len(self._clients)}"
        self._event_bus.publish(ClientConnected(client.nick))
        self._clients.add(client)

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                msg = f"ECHO: {data.decode().strip()}".encode()
                writer.write(msg)
                await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionResetError) as e:
            LOGGER.warning(f"Client disconnected unexpectedly: {addr} - {e}")
        except asyncio.CancelledError:
            pass
        finally:
            self._event_bus.publish(ClientDisconnected(client.nick))
            await client.disconnect()
            self._clients.remove(client)
            print(f"DISCONNECTED: {addr}")

    async def _start(self) -> None:
        self._server = await asyncio.start_server(
            self._handle_client, self.HOST, self._port
        )
        async with self._server:
            try:
                await self._server.serve_forever()
            except asyncio.CancelledError:
                LOGGER.info("Cancelling server loop")

    async def _disconnect_clients(self) -> None:
        for client in self._clients:
            await client.disconnect()
        self._clients.clear()

    def stop(self) -> None:
        LOGGER.info("Shutting down...")

        async def shutdown() -> None:
            await self._disconnect_clients()
            if self._server:
                self._server.close()
                await self._server.wait_closed()

        shutdown_status = asyncio.run_coroutine_threadsafe(shutdown(), self._loop)
        shutdown_status.result()

        self._loop.call_soon_threadsafe(self._loop.stop)
        LOGGER.info("Shut down")
        self._self_t.join()
