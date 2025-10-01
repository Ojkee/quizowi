import asyncio
import logging
import threading
from typing import Optional

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

    def __init__(self, port: int, max_room: int = 6) -> None:
        self._port: int = port
        self._max_room: int = max_room

        self._loop = asyncio.new_event_loop()
        self._self_t = threading.Thread(target=self._run_loop, daemon=True)

        self._clients: dict[asyncio.StreamReader, ConnectedClient] = {}
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
        self._clients[reader] = ConnectedClient(writer)

    async def _start(self) -> None:
        self._server = await asyncio.start_server(
            self._handle_client, self.HOST, self._port
        )
        async with self._server:
            try:
                await self._server.serve_forever()
            except asyncio.CancelledError:
                pass

    async def _disconnect_clients(self) -> None:
        for _, client in self._clients.items():
            await client.disconnect()
        self._clients.clear()

    def stop(self) -> None:
        LOGGER.info("Shutting down...")

        async def shutdown() -> None:
            if self._server:
                self._server.close()
                await self._server.wait_closed()
            await self._disconnect_clients()

        shutdown_status = asyncio.run_coroutine_threadsafe(shutdown(), self._loop)
        shutdown_status.result()

        self._loop.call_soon_threadsafe(self._loop.stop)

    def join(self) -> None:
        self._self_t.join()
