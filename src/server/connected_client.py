import asyncio


class ConnectedClient:
    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer

        self.nick: str = ""

    async def disconnect(self) -> None:
        self._writer.close()
        await self._writer.wait_closed()
