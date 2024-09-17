import asyncio


class IncomingMessage:
    def __init__(self, _join_ref, msg_ref, topic, event, payload):
        self.event = event
        self.topic = topic
        self.payload = payload
        self.ref = msg_ref

    def reply(self, event, payload):
        return OutgoingMessage(None, self.ref, self.topic, event, payload)


class OutgoingMessage:
    def __init__(self, join_ref, msg_ref, topic, event, payload):
        self.event = event
        self.topic = topic
        self.payload = payload
        self.ref = msg_ref
        self.join_ref = join_ref
        self.sent = asyncio.Future()

    def send(self, socket):
        socket.send(self)
        return self.sent
