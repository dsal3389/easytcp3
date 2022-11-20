import asyncio
from typing import Tuple, Type, Any
from easytcp.core.hooks import HookFactory
from .components.user import UserBase, User as BuiltinUser


class Server:

    def __init__(
        self, 
        ip: str, 
        port: int, 
        user_class: Type[UserBase]=BuiltinUser,
    ) -> None:
        self._ip = ip
        self._port = port
        self._user_class = user_class
        self._hook_factory = HookFactory()
        self._users = []

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    @property
    def hook(self) -> HookFactory:
        return self._hook_factory

    @property
    def users(self) -> Tuple[UserBase]:
        return tuple(self._users)

    async def run(self) -> None:
        server = await asyncio.start_server(
            self._connection_handler,
            host=self.ip, port=self.port
        )
        async with server:
            await server.serve_forever()

    async def _connection_handler(
        self, 
        reader: asyncio.StreamReader, 
        writer: asyncio.StreamWriter
    ) -> None:
        #while (id := self._generate_id()) in self._users:
        #    pass
        user = self._user_class(reader=reader, writer=writer)
        self._users.append(user)

        await self._hook_factory.call("client_connect", user=user)
        asyncio.create_task(user.listen(
            lambda *args, **kwargs: self._on_message_hanler(user=user, *args, **kwargs)
        ))
    
    async def _on_message_handler(self, message: Any) -> None:
        await self.hook.call(on_message, user=user, message=message)




