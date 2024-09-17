"""
Asynchronous client for the websocket interface.
"""

import asyncio

from .messages import OutgoingMessage
from .socket import Socket
from .utils import get_unless_done


class AsyncClient:
    def __init__(self, endpoint: str, app):
        from .. import client

        self.app = app
        self.endpoint = "ws" + endpoint[4:]
        self.iam_client = client("iam", app)
        self._ref = 1
        self._pending_queue = asyncio.Queue()

    async def connect(self):
        params = {"token": self.iam_client.get_token()}

        self.socket = Socket(
            f"{self.endpoint}/api/socket/websocket", params, self._pending_queue
        )
        self._done_recv = asyncio.Future()
        await self.socket.connect()

    async def disconnect(self):
        await self.socket.disconnect()

    async def stop(self):
        self._done_recv.set_result(True)
        await self.socket.stop()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def join(self, topic):
        message = OutgoingMessage(self._ref, None, topic, "phx_join", {})
        self._ref += 1
        await message.send(self.socket)

    async def send(self, event, topic, payload, ref=None):
        if ref is None:
            ref = self._ref
            self._ref += 1
        message = OutgoingMessage(None, ref, topic, event, payload)
        await message.send(self.socket)

    async def receive(self):
        msg = await get_unless_done(self._pending_queue.get(), self._done_recv)

        return msg
