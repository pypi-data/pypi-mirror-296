import asyncio
import json
from urllib.parse import urlencode

import websockets

from .messages import IncomingMessage
from .utils import DONE, get_unless_done


def _load_incoming_message(data):
    return IncomingMessage(*data)


def dump_outgoing_message(message):
    return [
        message.join_ref,
        message.ref,
        message.topic,
        message.event,
        message.payload,
    ]


class Transport:
    def __init__(self, url, params, incoming_queue, outgoing_queue):
        self.incoming_queue = incoming_queue
        self.outgoing_queue = outgoing_queue
        qs_params = {"vsn": "2.0.0", **params}
        self.url = url + "?" + urlencode(qs_params)
        self.ready = asyncio.Future()
        self._done = asyncio.Future()

    async def run(self):
        try:
            async with websockets.connect(self.url) as websocket:
                self.ready.set_result(True)
                await asyncio.gather(
                    self._recv_loop(websocket), self._send_loop(websocket)
                )
        except Exception as e:
            if not self.ready.done():
                self.ready.set_exception(e)

            raise

    async def stop(self):
        self._done.set_result(True)
        return True

    async def _recv_loop(self, websocket):
        while True:
            message_data = await get_unless_done(websocket.recv(), self._done)
            if message_data is DONE:
                return

            message = _load_incoming_message(json.loads(message_data))
            await self.incoming_queue.put(message)

    async def _send_loop(self, websocket):
        while True:
            message = await get_unless_done(self.outgoing_queue.get(), self._done)

            if message is DONE:
                return

            try:
                message_data = json.dumps(dump_outgoing_message(message))

                await websocket.send(message_data)
                message.sent.set_result(True)
            except Exception as e:
                print(e)
                message.sent.set_exception(e)
