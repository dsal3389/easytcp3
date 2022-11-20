import asyncio
from typing import Union, Callable


class Protocol:

    def __init__(
        self, 
        reader: asyncio.StreamReader, 
        writer: asyncio.StreamWriter
    ) -> None:
        self._reader = reader
        self._writer = writer 

    @property
    def reader(self) -> asyncio.StreamReader:
        return self.reader
        
    @property
    def writer(self) -> asyncio.StreamWriter:
        return self._writer

    async def listen(self, callback: Callable) -> None:
        while True:
            data = await self.recv()
            if not data:
                break
            await callback(data)

    async def send(self, data: str, drain=True) -> None:
        data = self.parse_send_data(data)
        self._writer.write(data)

        if drain:
            await self._writer.drain()

    async def recv(self, size=-1) -> bytes:
        data = await self._reader.read(size)
        return self.parse_recv_data(data)

    def parse_send_data(self, data: str) -> bytes:
        return bytes(data, encoding="utf-8")

    def parse_recv_data(self, data: bytes) -> Any:
        return str(bytes, encoding='utf-8')


