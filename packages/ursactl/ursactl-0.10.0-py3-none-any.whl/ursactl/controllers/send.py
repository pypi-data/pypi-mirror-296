import json
import sys

import yaml
from cement import Controller, ex

from ..core.services import client


class Send(Controller):
    """
    Provides the 'send' verb.
    """

    class Meta:
        label = "send"
        stacked_on = "base"
        stacked_type = "nested"
        help = "send something"

    @ex(
        help="send a message to an agent",
        arguments=[
            (["--test", "-t"], {"help": "test mode", "action": "store_true"}),
            (["id"], {"help": "agent instance identifier", "action": "store"}),
            (
                ["events"],
                {"help": "file containing message(s) to send", "action": "store"},
            ),
        ],
    )
    def agent_event(self):
        planning_client = client("planning", self.app)
        file = self.app.pargs.events
        if file == "-":
            # we assume that this is a one-shot set of events, so we read until STDIN closes
            content = sys.stdin.read()
            # read with YAML since that's a superset of JSON
            events = self._yaml_load(content)
        else:
            if file.endswith(".yaml") or file.endswith(".yml"):
                loader = self._yaml_load
            elif file.endswith(".json"):
                loader = json.load
            else:
                print("Only YAML and JSON files may be uploaded.")
                sys.exit(1)
            with open(file, "r", encoding="utf-8") as fd:
                events = loader(fd)

        if not isinstance(events, list):
            events = [events]
        method = planning_client.send_event_to_agent
        if self.app.pargs.test:
            method = planning_client.test_event_with_agent
        for event in events:
            result = method(self.app.pargs.id, event)
            self._print(result)

    @ex(
        help="send a message to an agent swarm",
        arguments=[
            (["id"], {"help": "agent swarm identifier", "action": "store"}),
            (
                ["events"],
                {"help": "file containing message(s) to send", "action": "store"},
            ),
        ],
    )
    def agent_swarm_event(self):
        planning_client = client("planning", self.app)
        file = self.app.pargs.events
        if file == "-":
            # we assume that this is a one-shot set of events, so we read until STDIN closes
            content = sys.stdin.read()
            # read with YAML since that's a superset of JSON
            events = self._yaml_load(content)
        else:
            if file.endswith(".yaml") or file.endswith(".yml"):
                loader = self._yaml_load
            elif file.endswith(".json"):
                loader = json.load
            else:
                print("Only YAML and JSON files may be uploaded.")
                sys.exit(1)
            with open(file, "r", encoding="utf-8") as fd:
                events = loader(fd)

        if not isinstance(events, list):
            events = [events]
        for event in events:
            result = planning_client.send_event_to_agent_swarm(self.app.pargs.id, event)
            self._print(result)

    @staticmethod
    def _yaml_load(fd):
        return list(yaml.load_all(fd, Loader=yaml.Loader))

    def _print(self, data):
        if self.app.pargs.output == "json":
            print(json.dumps(data))
        else:
            print(yaml.dump(data))

    @property
    def _project_scope(self):
        return self.app.pargs.project or self.app.config.get("ursactl", "project")
