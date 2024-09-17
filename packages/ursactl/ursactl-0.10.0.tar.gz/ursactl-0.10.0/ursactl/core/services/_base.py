"""
Base class for API clients.
"""

import configparser
import re

import requests
from python_graphql_client import GraphqlClient

from ursactl.core.exc import UrsaNotAuthorized


class Base:
    """
    Base class for clients.
    """

    def __init__(self, endpoint: str, app):
        from .. import services

        self.app = app
        self.endpoint = endpoint
        self.iam_client = services.client("iam", app)
        self.client = GraphqlClient(endpoint=f"{endpoint}api", timeout=self.timeout)

    def raw_query(self, query, variables=None, reauthorize=True):
        if variables is None:
            variables = {}

        try:
            result = self.client.execute(
                query=query,
                variables=variables,
                headers={"authorization": f"Bearer {self.iam_client.get_token()}"},
            )

            if "errors" in result:
                for error in result["errors"]:
                    if "code" in error and error["code"] == "Forbidden":
                        if reauthorize:
                            self.iam_client.clear_token()
                            return self.raw_query(query, variables, reauthorize=False)
                        raise UrsaNotAuthorized("Not authorized")

                    print(error["message"])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                if reauthorize:
                    self.iam_client.clear_token()
                    return self.raw_query(query, variables, reauthorize=False)
                raise UrsaNotAuthorized("Not authorized") from e

            raise e
        return result

    @property
    def timeout(self):
        return (
            self._get_arg("connect_timeout", 60.0),
            self._get_arg("read_timeout", 60.0),
        )

    def _get_arg(self, key, default):
        try:
            pargs = vars(self.app.pargs)
            value = pargs[key]
        except AttributeError:
            value = None
        except TypeError:
            value = None

        if value is None:
            try:
                value = self.app.config.get("ursactl", key)
            except configparser.NoOptionError:
                value = default
        return float(value)

    @staticmethod
    def is_uuid(s: str) -> bool:
        """
        Test if the string looks like a UUID.
        """
        if s is None:
            return False
        return re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", s
        )
