import threading
import asyncio
from typing import Optional


class ClientSocket:
    def __init__(self, ip: str, port: int) -> None:
        self._ip: str = ip
        self._port = port
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = asyncio.Event()

        self._loop = asyncio.new_event_loop()
        self._self_t = threading.Thread(target=self._run_loop, daemon=True)

    def connect(self) -> None:
        self._self_t.start()

    async def _connect(self) -> None:
        self._reader, self._writer = await asyncio.open_connection(self._ip, self._port)
        self._connected.set()

        await self._listener()

        self._writer.close()
        await self._writer.wait_closed()
        self._writer = None
        print("disconnected")  # TODO: remove

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

    def _run_loop(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.create_task(self._connect())
        self._loop.run_forever()

    async def send(self, message: str) -> None:
        await self._connected.wait()
        if not self._writer:
            return
        self._writer.write(message.encode("utf-8"))
        await self._writer.drain()

    def stop(self) -> None:
        async def shutdown():
            if self._writer:
                self._writer.close()
                await self._writer.wait_closed()
                self._writer = None

        shutdown_status = asyncio.run_coroutine_threadsafe(shutdown(), self._loop)
        shutdown_status.result()

        self._loop.call_soon_threadsafe(self._loop.stop)
        self._self_t.join()
