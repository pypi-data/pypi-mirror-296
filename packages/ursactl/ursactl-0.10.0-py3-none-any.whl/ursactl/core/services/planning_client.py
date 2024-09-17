"""
Planning capabilities client.
"""

import json

from ursactl.core.exc import UrsaBadProjectName

from ._base import Base

LIST_PACKAGES_QUERY = """\
query list_packages($id: String!) {
    project(handleName: $id) {
        packages {
            id
            name
            isSynced
        }
    }
}
"""

LIST_AGENTS_QUERY = """\
query list_packages($id: String!) {
    project(handleName: $id) {
        agents {
            id
            name
            isSynced
        }
    }
}
"""

LIST_AGENT_SWARMS_QUERY = """\
query list_packages($id: String!) {
    project(handleName: $id) {
        agent_swarms {
            id
            name
        }
    }
}
"""

CREATE_PACKAGE_MUTATION = """\
mutation create_package($input: CreatePackageInput!) {
    createPackage(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

SYNC_PACKAGE_MUTATION = """\
mutation sync_package($input: SyncPackageInput!) {
    syncPackage(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

UPDATE_PACKAGE_MUTATION = """\
mutation update_package($input: UpdatePackageInput!) {
    updatePackage(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

GET_PACKAGE_BY_NAME = """\
query get_package($name: String!, $project_id: String!) {
    project(handleName: $project_id) {
        packages(limit: 1, filter: { name: { eq: $name } }) {
            id
            name
        }
    }
}
"""

GET_PACKAGE_BY_ID = """\
query get_package($id: ID!) {
    package(id: $id) {
        id
        name
    }
}
"""

DELETE_PACKAGE_MUTATION = """\
mutation delete_package($id: ID!) {
    deletePackage(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

DELETE_SYNCED_PACKAGE_MUTATION = """\
mutation delete_synced_package($id: ID!) {
    deleteSyncedPackage(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

CREATE_AGENT_MUTATION = """\
mutation create_agent($input: CreateAgentInput!) {
    createAgent(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

SYNC_AGENT_MUTATION = """\
mutation sync_agent($input: SyncAgentInput!) {
    syncAgent(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

DELETE_AGENT_MUTATION = """\
mutation delete_agent($id: ID!) {
    deleteAgent(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

DELETE_SYNCED_AGENT_MUTATION = """\
mutation delete_synced_agent($id: ID!) {
    deleteSyncedAgent(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

GET_AGENT_BY_NAME = """\
query get_agent($name: String!, $project_id: String!) {
    project(handleName: $project_id) {
        agents(limit: 1, filter: { name: { eq: $name } }) {
            id
            name
        }
    }
}
"""

GET_AGENT_BY_ID = """\
query get_agent($id: ID!) {
    agent(id: $id) {
        id
        name
    }
}
"""

GET_AGENT_SWARM_BY_NAME = """\
query get_agent_swarm($name: String!, $project_id: String!) {
    project(handleName: $project_id) {
        agentSwarms(limit: 1, filter: { name: { eq: $name } }) {
            id
            name
        }
    }
}
"""

GET_AGENT_SWARM_BY_ID = """\
query get_agent_swarm($id: ID!) {
    agentSwarm(id: $id) {
        id
        name
    }
}
"""

RUN_AGENT_MUTATION = """\
mutation run_agent($input: RunAgentInput!) {
    runAgent(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
        }
    }
}
"""

STOP_AGENT_MUTATION = """\
mutation stop_agent($id: ID!) {
    stopAgent(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
        }
    }
}
"""

CREATE_AGENT_SWARM_MUTATION = """\
mutation create_agent_swarm($input: CreateAgentSwarmInput!) {
    createAgentSwarm(input: $input) {
        errors {
            code
            message
            fields
        }
        result {
            id
        }
    }
}
"""

DELETE_AGENT_SWARM_MUTATION = """\
mutation delete_agent_swarm($id: ID!) {
    deleteAgentSwarm(id: $id) {
        errors {
            code
            message
            fields
        }
        result {
            id
            name
        }
    }
}
"""

RUN_AGENTS_IN_SWARM_MUTATION = """\
mutation run_agents_in_swarm($agentSwarmId: ID!, $agent: String!, $groups: [String], $params: [AgentState]) {
    runAgentsInSwarm(agent: $agent, agentSwarmId: $agentSwarmId, groups: $groups, params: $params) {
        errors {
            code
            message
            fields
        }
        result
    }
}
"""

LIST_RUNNING_AGENTS_BY_PROJECT = """\
query list_agents_by_project($id: String!) {
    project(handleName: $id) {
        agents {
            name
            runningAgents {
                id
                startedAt
                status
            }
        }
    }
}
"""

LIST_RUNNING_AGENTS_BY_AGENT = """\
query list_agents_by_agent($id: ID!) {
    agent(id: $id) {
        name
        runningAgents {
            id
            startedAt
            status
        }
    }
}
"""

SEND_EVENT_TO_AGENT_MUTATION = """\
mutation send_event($agentId: ID!, $domain: String!, $name: String!, $params: Json!) {
  sendEventToAgent(agentId:$agentId,domain:$domain,name:$name,params:$params) {
    errors {
        code
        message
        fields
    }
    result {
        domain
        name
        params
    }
  }
}
"""

TEST_EVENT_WITH_AGENT_MUTATION = """\
mutation test_event($agentId: ID!, $domain: String!, $name: String!, $params: Json) {
    testEventWithAgent(agentId:$agentId,domain:$domain,name:$name,params:$params) {
        errors {
            code
            message
            fields
        }
        result
    }
}
"""

SEND_EVENT_TO_AGENT_SWARM_MUTATION = """\
        mutation send_event($agentSwarmId: ID!, $domain: String!, $name: String!, $params: Json!, $group: String) {
  sendEventToAgentSwarm(agentSwarmId:$agentSwarmId,domain:$domain,name:$name,params:$params,group:$group) {
    errors {
        code
        message
        fields
    }
    result {
        domain
        name
        params
    }
  }
}
"""


class PlanningClient(Base):
    """-
    Client providing access to the planning capabilities.
    """

    def list_packages(self, project_uuid=None):
        """
        Return a list of available packages.
        """

        query_response = self.raw_query(
            query=LIST_PACKAGES_QUERY, variables={"id": project_uuid}
        )
        if query_response["data"]["project"] is None:
            raise UrsaBadProjectName(project_uuid)
        return query_response["data"]["project"]["packages"]

    def list_agents(self, project_uuid=None):
        """
        Return a list of available agents.
        """
        query_response = self.raw_query(
            query=LIST_AGENTS_QUERY, variables={"id": project_uuid}
        )
        if query_response["data"]["project"] is None:
            raise UrsaBadProjectName(project_uuid)
        return query_response["data"]["project"]["agents"]

    def list_running_agents(self, agent_id=None, project_uuid=None):
        """
        Return a list of running agents.
        """
        if agent_id is not None:
            if self.is_uuid(agent_id):
                variables = {"id": agent_id}
            else:
                agent = self.get_agent(agent_id, project_uuid)
                if agent is None:
                    return []
                variables = {"id": agent["id"]}
            query_response = self.raw_query(
                query=LIST_RUNNING_AGENTS_BY_AGENT, variables=variables
            )
            agent_name = query_response["data"]["agent"]["name"]
            return [
                {"agent": agent_name, **info}
                for info in query_response["data"]["agent"]["runningAgents"]
            ]

        elif project_uuid is not None:
            query_response = self.raw_query(
                query=LIST_RUNNING_AGENTS_BY_PROJECT, variables={"id": project_uuid}
            )
            if query_response["data"]["project"] is None:
                raise UrsaBadProjectName(project_uuid)
            return [
                {"agent": agent["name"], **info}
                for agent in query_response["data"]["project"]["agents"]
                for info in agent["runningAgents"]
            ]

    def list_agent_swarms(self, project_uuid=None):
        """
        Return a list of available agents.
        """
        query_response = self.raw_query(
            query=LIST_AGENT_SWARMS_QUERY, variables={"id": project_uuid}
        )
        if query_response["data"]["project"] is None:
            raise UrsaBadProjectName(project_uuid)
        return query_response["data"]["project"]["agent_swarms"]

    def create_package(self, project_uuid=None, content=None):
        """
        Create a new package.
        """
        mutation_response = self.raw_query(
            query=CREATE_PACKAGE_MUTATION,
            variables={"input": {"source": content, "project": project_uuid}},
        )
        return mutation_response["data"]["createPackage"]

    def sync_package(self, project_uuid=None, content=None):
        """
        Sync a new package.
        """
        mutation_response = self.raw_query(
            query=SYNC_PACKAGE_MUTATION,
            variables={"input": {"source": content, "project": project_uuid}},
        )
        return mutation_response["data"]["syncPackage"]

    def update_package(self, project_uuid=None, content=None):
        """
        Update an existing package.
        """
        mutation_response = self.raw_query(
            query=UPDATE_PACKAGE_MUTATION,
            variables={"input": {"source": content, "project": project_uuid}},
        )
        return mutation_response["data"]["updatePackage"]

    def create_agent(self, project_uuid=None, name=None, packages=None, behaviors=None):
        """
        Create a new agent.
        """
        mutation_response = self.raw_query(
            query=CREATE_AGENT_MUTATION,
            variables={
                "input": {
                    "name": name,
                    "packages": packages,
                    "behaviors": behaviors,
                    "project": project_uuid,
                }
            },
        )
        return mutation_response["data"]["createAgent"]

    def sync_agent(self, project_uuid=None, name=None, packages=None, behaviors=None):
        """
        Sync an agent.
        """
        mutation_response = self.raw_query(
            query=SYNC_AGENT_MUTATION,
            variables={
                "input": {
                    "name": name,
                    "packages": packages,
                    "behaviors": behaviors,
                    "project": project_uuid,
                }
            },
        )
        return mutation_response["data"]["syncAgent"]

    def create_agent_swarm(self, project_uuid=None, name=None):
        """
        Create a new swarm.
        """
        mutation_response = self.raw_query(
            query=CREATE_AGENT_SWARM_MUTATION,
            variables={"input": {"name": name, "project": project_uuid}},
        )
        return mutation_response["data"]["createAgentSwarm"]

    def get_package(self, name=None, project_uuid=None):
        """
        Get the id and basic info about a package.
        """
        if self.is_uuid(name):
            variables = {"id": name}
            query = GET_PACKAGE_BY_ID
        else:
            variables = {"name": name, "project_id": project_uuid}
            query = GET_PACKAGE_BY_NAME
        result = self.raw_query(query=query, variables=variables)
        if query == GET_PACKAGE_BY_ID:
            return result["data"]["package"]
        return result["data"]["project"]["packages"][0]

    def get_agent(self, name=None, project_uuid=None):
        """
        Get the id and basic info about an agent.
        """
        if self.is_uuid(name):
            variables = {"id": name}
            query = GET_AGENT_BY_ID
        else:
            variables = {"name": name, "project_id": project_uuid}
            query = GET_AGENT_BY_NAME
        result = self.raw_query(query=query, variables=variables)
        if query == GET_AGENT_BY_ID:
            return result["data"]["agent"]

        return result["data"]["project"]["agents"][0]

    def get_agent_swarm(self, name=None, project_uuid=None):
        """
        Get the id and basic info about an agent swarm.
        """
        if self.is_uuid(name):
            variables = {"id": name}
            query = GET_AGENT_SWARM_BY_ID
        else:
            variables = {"name": name, "project_id": project_uuid}
            query = GET_AGENT_SWARM_BY_NAME
        result = self.raw_query(query=query, variables=variables)
        if query == GET_AGENT_SWARM_BY_ID:
            return result["data"]["agentSwarm"]

        return result["data"]["project"]["agentSwarms"][0]

    def delete_package(self, package_id, project_uuid=None):
        """
        Deletes a package.
        """
        if self.is_uuid(package_id):
            variables = {"id": package_id}
        else:
            package = self.get_package(name=package_id, project_uuid=project_uuid)
            if package is None:
                return {}
            variables = {"id": package["id"]}

        result = self.raw_query(query=DELETE_PACKAGE_MUTATION, variables=variables)

        return result["data"]["deletePackage"]

    def delete_synced_package(self, package_id, project_uuid=None):
        """
        Deletes a synced package.
        """
        if self.is_uuid(package_id):
            variables = {"id": package_id}
        else:
            package = self.get_package(name=package_id, project_uuid=project_uuid)
            if package is None:
                return {}
            variables = {"id": package["id"]}

        result = self.raw_query(
            query=DELETE_SYNCED_PACKAGE_MUTATION, variables=variables
        )

        return result["data"]["deleteSyncedPackage"]

    def delete_agent(self, agent_id, project_uuid=None):
        """
        Deletes an agent.
        """
        if self.is_uuid(agent_id):
            variables = {"id": agent_id}
        else:
            agent = self.get_agent(name=agent_id, project_uuid=project_uuid)
            if agent is None:
                return {}
            variables = {"id": agent["id"]}

        result = self.raw_query(query=DELETE_AGENT_MUTATION, variables=variables)

        return result["data"]["deleteAgent"]

    def delete_agent_swarm(self, agent_swarm_id, project_uuid=None):
        """
        Deletes an agent swarm.
        """
        if self.is_uuid(agent_swarm_id):
            variables = {"id": agent_swarm_id}
        else:
            agent = self.get_agent_swarm(name=agent_swarm_id, project_uuid=project_uuid)
            if agent is None:
                return {}
            variables = {"id": agent["id"]}

        result = self.raw_query(query=DELETE_AGENT_SWARM_MUTATION, variables=variables)

        return result["data"]["deleteAgentSwarm"]

    def delete_synced_agent(self, agent_id, project_uuid=None):
        """
        Deletes a synced agent.
        """
        if self.is_uuid(agent_id):
            variables = {"id": agent_id}
        else:
            agent = self.get_agent(name=agent_id, project_uuid=project_uuid)
            if agent is None:
                return {}
            variables = {"id": agent["id"]}

        result = self.raw_query(query=DELETE_SYNCED_AGENT_MUTATION, variables=variables)

        return result["data"]["deleteSyncedAgent"]

    def run_agent(
        self, agent_id, project_uuid=None, initial_predicates=None, initial_state=None
    ):
        """
        Runs an agent.
        """
        variables = {"input": {"project": project_uuid}}
        if self.is_uuid(agent_id):
            agent = self.get_agent(name=agent_id, project_uuid=project_uuid)
            if agent is None:
                return {}
            variables["input"]["agent"] = agent["name"]
        else:
            agent = self.get_agent(name=agent_id, project_uuid=project_uuid)
            if agent is None:
                return {}
            variables["input"]["agent"] = agent_id

        if initial_state is not None:
            variables["input"]["initialState"] = initial_state
        if initial_predicates is not None:
            variables["input"]["initialPredicates"] = initial_predicates

        result = self.raw_query(query=RUN_AGENT_MUTATION, variables=variables)

        return result["data"]["runAgent"]

    def run_agents_in_swarm(self, agent_swarm_id, agent_name, configs, groups=[]):
        """
        Runs agents in an agent swarm.
        """
        variables = {
            "agent": agent_name,
            "agentSwarmId": agent_swarm_id,
            "params": configs,
        }
        if groups:
            variables["groups"] = groups
        result = self.raw_query(query=RUN_AGENTS_IN_SWARM_MUTATION, variables=variables)

        return result["data"]["runAgentsInSwarm"]

    def send_event_to_agent(self, agent_instance_id, event):
        """
        Sends an event to an agent.
        """
        variables = {"agentId": agent_instance_id, **event}
        variables["params"] = json.dumps(variables["params"])

        result = self.raw_query(query=SEND_EVENT_TO_AGENT_MUTATION, variables=variables)

        return result["data"]["sendEventToAgent"]

    def test_event_with_agent(self, agent_instance_id, event):
        """
        Sends an event to an agent to test planning.
        """
        variables = {"agentId": agent_instance_id, **event}
        variables["params"] = json.dumps(variables["params"])

        result = self.raw_query(query=TEST_EVENT_WITH_AGENT_MUTATION, variables=variables)

        return result["data"]["testEventWithAgent"]

    def stop_agent(self, agent_id):
        """
        Stops an agent.
        """
        variables = {"id": agent_id}

        result = self.raw_query(query=STOP_AGENT_MUTATION, variables=variables)

        return result["data"]["stopAgent"]

    def send_event_to_agent_swarm(self, agent_swarm_id, event):
        """
        Sends an event to an agent swarm.
        """
        variables = {"agentSwarmId": agent_swarm_id, **event}
        variables["params"] = json.dumps(variables["params"])

        result = self.raw_query(
            query=SEND_EVENT_TO_AGENT_SWARM_MUTATION, variables=variables
        )

        return result["data"]["sendEventToAgentSwarm"]
