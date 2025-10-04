import sys
import asyncio


class ClientSocket:
    def __init__(self, port: int) -> None:
        self._port = port

    async def _connect(self) -> None:
        reader, writer = await asyncio.open_connection("localhost", self._port)

        listener = asyncio.create_task(self._listener(reader))
        sender = asyncio.create_task(self._sender(writer))

        _, pending = await asyncio.wait(
            {listener, sender}, return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

        writer.close()
        await writer.wait_closed()
        print("disconnected")

    async def _listener(self, reader: asyncio.StreamReader) -> None:
        try:
            while True:
                server_msg = await reader.read(1024)
                if not server_msg:
                    break
                print(server_msg)
        except asyncio.CancelledError:
            pass

    async def _sender(self, writer: asyncio.StreamWriter) -> None:
        try:
            while True:
                msg = await self._wait_for_input("> ")
                if msg.lower() == "quit":
                    break
                writer.write(msg.encode())
                await writer.drain()
        except asyncio.CancelledError:
            pass

    async def _wait_for_input(self, ss: str) -> str:
        sys.stdout.write(ss)
        sys.stdout.flush()
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    def connect(self) -> None:
        asyncio.run(self._connect())
