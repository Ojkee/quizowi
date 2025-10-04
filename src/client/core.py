import asyncio
from typing import Optional


class ClientSocket:
    def __init__(self, port: int) -> None:
        self._port = port
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = asyncio.Event()

    async def _connect(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(
            "localhost", self._port
        )
        self._connected.set()

        await self._listener()

        self._writer.close()
        await self._writer.wait_closed()
        print("disconnected")

    async def _listener(self) -> None:
        try:
            while True:
                server_msg = (
                    await self._reader.read(1024)
                    if self._reader
                    else b"Not connected yet"
                )
                if not server_msg:
                    break
                print(server_msg.decode("utf-8"))
        except asyncio.CancelledError:
            pass

    def connect(self) -> None:
        asyncio.run(self._connect())

    async def send(self, message: str) -> None:
        await self._connected.wait()
        if not self._writer:
            return
        self._writer.write(message.encode("utf-8"))
        await self._writer.drain()

    def stop(self) -> None:
        # TODO: implement disconnection
        pass
