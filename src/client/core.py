import asyncio


class ClientSocket:
    def __init__(self, port: int) -> None:
        self._port = port

    async def _connect(self) -> None:
        reader, writer = await asyncio.open_connection("localhost", self._port)

        writer.write(b"hello")
        await writer.drain()

        data = await reader.read(100)
        print(data.decode("utf-8"))

        writer.close()
        await writer.wait_closed()

    def connect(self) -> None:
        asyncio.run(self._connect())
