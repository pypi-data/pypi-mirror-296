import asyncio

from .transport import Transport

# from .messages import IncomingMessage, OutgoingMessage
from .utils import DONE, get_unless_done


class Socket:
    def __init__(self, url, params, pending_queue):
        self.url = url
        self.params = params
        self._incoming_queue = asyncio.Queue()
        self._outgoing_queue = asyncio.Queue()
        self._pending_queue = pending_queue
        self.connected = False
        self._response_futures = {}

    async def connect(self):
        if self.connected:
            raise Exception("Already connected")

        self.transport = Transport(
            self.url, self.params, self._incoming_queue, self._outgoing_queue
        )
        transport_task = asyncio.ensure_future(self.transport.run())
        await self.transport.ready

        self._transport_task = transport_task
        self._done_recv = asyncio.Future()
        self._recv_task = asyncio.ensure_future(self._recv_loop())
        self.connected = True

    async def disconnect(self):
        if self.connected:
            self._done_recv.set_result(True)

            await asyncio.gather(self._recv_task, self._transport_task)
            await self.transport.stop()

            self.connected = False

    async def stop(self):
        await self.disconnect()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def _recv_loop(self):
        while True:
            message = await get_unless_done(self._incoming_queue.get(), self._done_recv)
            if message is DONE:
                return

            if message.ref in self._response_futures:
                future = self._response_futures.pop(message.ref)
                future.set_result(message.payload)
            else:
                self._pending_queue.put_nowait(message)

    def send(self, message):
        if not self.connected:
            raise Exception("Not connected")
        self._outgoing_queue.put_nowait(message)
        return message.sent
