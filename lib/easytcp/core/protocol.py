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

    async def send(self, data: Union[bytes, str]) -> None:
        if isinstance(data, str):
            data = bytes(data, encoding="utf-8")

        self._writer.write(data)
        await self._writer.drain()

    async def recv(self, size=-1) -> bytes:
        return await self._reader.read(size)


