"""
IAM API client.
"""

import configparser
import sys

import requests
from requests.auth import HTTPBasicAuth
from tinydb import Query


class IamClient:
    """
    A client for accessing IAM functions in the Ursa Frontier platform.

    This is limited to using API credentials to get a token that can be
    used with other platform services.
    """

    def __init__(self, endpoint: str, app):
        self.app = app
        self.endpoint = endpoint

    def clear_token(self):
        """
        Used to remove a cached token when it doesn't work.
        """
        try:
            api_key = self.app.config.get("ursactl", "api_key")
        except configparser.NoOptionError:
            print(
                "You need to set the api_key and api_secret in the ursactl.conf file."
            )
            sys.exit(1)

        query = Query()
        self.app.db.remove(query.api_key == api_key)

    def get_token(self):
        """
        Retrieves a token that can be used with other services.
        """
        try:
            api_key = self.app.config.get("ursactl", "api_key")
            api_secret = self.app.config.get("ursactl", "api_secret")
        except configparser.NoOptionError:
            print(
                "You need to set the api_key and api_secret in the ursactl.conf file."
            )
            sys.exit(1)

        # check if it's in the tinydb -- if so, return it
        query = Query()
        results = self.app.db.search(query.api_key == api_key)

        if results:
            return results[0]["token"]

        # otherwise, get a token, save it to tinydb, and then return it
        response = requests.get(
            f"{self.endpoint}api/token",
            auth=HTTPBasicAuth(api_key, api_secret),
            timeout=self.timeout,
        )

        if response.status_code != 200:
            return

        token = response.json()["token"]
        self.app.db.insert({"api_key": api_key, "token": token})
        return token

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
