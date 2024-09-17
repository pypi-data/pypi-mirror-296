import asyncio

from ursactl.core._base import Base
from ursactl.core.services import client

from .running_agent import RunningAgent
from .services.async_client.utils import DONE


class AgentSwarm(Base):
    """
    Provides access to agent swarms.
    """

    @property
    def client(self):
        if self._client is None:
            self._client = client("planning", self.app)
        return self._client

    @property
    def name(self):
        return self._data["name"]

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {"name": None, "project_uuid": None}
            else:
                self._cached_data = self.client.get_agent_swarm(self.uuid)
        return self._cached_data

    def send_event(self, domain, name, params, group=None):
        result = self.client.send_event_to_agent_swarm(
            self.uuid,
            {"domain": domain, "name": name, "params": params, "group": group},
        )
        return result["result"]

    def send_events(self, events):
        actions = []
        for event in events:
            result = self.client.send_event_to_agent_swarm(self.uuid, event)
            if result["result"]:
                actions.extend(result["result"])
        return actions

    def add_agents(self, agent_name, configs, groups=[]):
        result = self.client.run_agents_in_swarm(self.uuid, agent_name, configs, groups)
        if result["errors"]:
            return None
        return [
            RunningAgent(
                uuid=running_agent_id,
                app=self.app,
                client=self.client,
                project=self.project,
            )
            for running_agent_id in result["result"]
        ]

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.client.delete_agent_swarm(self.uuid)

    def for_async(self):
        return AsyncAgentSwarm(self)

    @classmethod
    def create_anonymous(klass, project=None, app=None, **_kwargs):
        c = client("planning", app)
        swarm = c.create_agent_swarm(project_uuid=project.uuid)
        return klass(uuid=swarm["result"]["id"], project=project, app=app, client=c)


class AsyncAgentSwarm(Base):
    def __init__(self, swarm):
        self.swarm = swarm
        self._app = swarm.app
        self._uuid = swarm.uuid
        self._client = None
        self._topic = f"swarm:{self._uuid}"
        self.project = swarm.project
        self._handlers = {}

    @property
    def client(self):
        if self._client is None:
            self._client = client("async", self.app)
        return self._client

    async def stop(self):
        await self.client.stop()
        return True

    def add_handler(self, domain, handler):
        print("Adding handler", domain, handler)
        try:
            self._handlers[domain].append(handler)
        except KeyError:
            self._handlers[domain] = [handler]
        print(self._handlers)

    async def connect(self):
        await self.client.connect()
        await self.client.join(self._topic)
        recv_task = asyncio.ensure_future(self.run())
        self._recv_task = recv_task

    async def disconnect(self):
        await asyncio.gather(self._recv_task)
        await self.client.disconnect()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def send_event(self, domain, name, params, group=None):
        print("Sending event", domain, name, params, group)
        await self.client.send(
            "event",
            self._topic,
            {"domain": domain, "name": name, "params": params, "group": group},
        )

    async def receive(self):
        return await self.client.receive()

    def add_agents(self, agent_name, configs, groups=[]):
        return self.swarm.add_agents(agent_name, configs, groups)

    async def _handle_action(self, message):
        payload = message.payload
        if payload["domain"] in self._handlers:
            handlers = self._handlers[payload["domain"]]
            for handler in handlers:
                try:
                    method = handler.__class__.actions.get(payload["name"])
                    events = await method(handler, payload["params"])
                    if events:
                        for event in events:
                            await self.send_event(
                                event.get("domain"),
                                event.get("name"),
                                event.get("params"),
                                event.get("group"),
                            )
                except Exception as e:
                    print(e)
                    pass

    async def _hande_perception(self, message):
        payload = message.payload
        handled = False
        if payload["domain"] in self._handlers:
            handlers = self._handlers[payload["domain"]]
            for handler in handlers:
                try:
                    method = handler.__class__.perceptions.get(payload["name"])
                    value = await method(handler, *payload["arguments"])
                    await self.client.send(
                        "perceived",
                        self._topic,
                        {
                            "domain": payload["domain"],
                            "name": payload["name"],
                            "arguments": payload["arguments"],
                            "value": value,
                        },
                    )

                    handled = True
                    break
                except Exception as e:
                    print(e)
                    pass
        if not handled:
            await self.client.send(
                "perceived",
                self._topic,
                {
                    "domain": payload["domain"],
                    "name": payload["name"],
                    "arguments": payload["arguments"],
                    "value": None,
                },
            )

    async def run(self):
        while True:
            message = await self.client.receive()
            if message == DONE:
                return
            if message.event.startswith("phx_"):
                print("Received phoenix message", message.event, message.payload)
                continue
            if message.event == "action":
                await self._handle_action(message)
                continue
            if message.event == "perceive":
                await self._hande_perception(message)
                continue

            print(f"Received message with unknown event: {message.event}")
