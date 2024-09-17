"""
Manages service discovery.
"""

from typing import Optional

from .ape_client import ApeClient
from .async_client.client import AsyncClient
from .dss_client import DssClient
from .iam_client import IamClient
from .page_client import PageClient
from .planning_client import PlanningClient
from .project_client import ProjectClient

SERVICE_CLIENTS = {
    "ape": ApeClient,
    "dss": DssClient,
    "page": PageClient,
    "iam": IamClient,
    "planning": PlanningClient,
    "projects": ProjectClient,
    "async": AsyncClient,
}


def client(service: Optional[str] = None, app=None):
    """
    Returns a client appropriate for the service. The optional `app` parameter
    allows the reuse of an UrsaCtl object to manage configuration.
    """
    if app is None:
        from ursactl.main import UrsaCtl

        app = UrsaCtl()
        app.reload()

    platform = app.config.get("ursactl", "platform")

    if service in SERVICE_CLIENTS:
        return SERVICE_CLIENTS[service](platform, app)
