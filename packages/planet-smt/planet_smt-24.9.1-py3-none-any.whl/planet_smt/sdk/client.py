"""Client for interaction with the SMT API."""

from __future__ import annotations

import datetime
from collections.abc import Callable
from functools import wraps
from logging import getLogger
from typing import Concatenate, ParamSpec, TypeVar

import httpx
from pydantic import BaseModel

from ..models.scope import ScopeConfigParams
from ..models.state import FlowRun
from ..models.workflow import FullFlowParams, RefdataFlowParams, SignalDownloadFlowParams
from ..utils import handle_http_status_errors

LOGGER = getLogger("planet_smt.client")

T = ParamSpec("T")
U = TypeVar("U")

BACKOFF_MAX_TIME = 180


class InvalidCredentialsError(Exception):
    """Exception raised when the provided user credentials are invalid."""


class TokenRefreshError(Exception):
    """Exception raised when the token refresh fails."""


class SessionExpiredError(Exception):
    """Exception raised when the refresh token has expired.
    User should try to log in again.
    """


class AuthenticationResponse(BaseModel):
    """Response model for the token acquisition endpoint."""

    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int


class UserCredentials:
    """Class for storing user credentials."""

    def __init__(self, auth_response: AuthenticationResponse) -> None:
        """Constructor for user credentials object. Stores timestamp of the token creation.
        Some buffer is also substracted from the expiry time.
        """
        timestamp = datetime.datetime.now()

        self.access_token = auth_response.access_token
        self.refresh_token = auth_response.refresh_token
        self.access_expiry = timestamp + datetime.timedelta(seconds=auth_response.expires_in - 30)
        self.refresh_expiry = timestamp + datetime.timedelta(seconds=auth_response.refresh_expires_in - 30)

    def access_expired(self) -> bool:
        """Check if the access token has expired."""
        return datetime.datetime.now() > self.access_expiry

    def refresh_expired(self) -> bool:
        """Check if the refresh token has expired."""
        return datetime.datetime.now() > self.refresh_expiry


def token_required(method: Callable[Concatenate[SMTClient, T], U]) -> Callable[Concatenate[SMTClient, T], U]:
    """Decorator for `SMTClient` methods that require a valid token.
    On the client side, tokens are validated for expiry before request is sent to the service.
    If the access token is expired, it will also be refreshed if the refresh token is still valid.
    """

    @wraps(method)
    def wrapper(
        client: SMTClient, /, *args: T.args, **kwargs: T.kwargs
    ) -> U:  # '/' is used to indicate positional-only arguments.
        """Wrapper function for token validation."""
        if not client.credentials.access_expired():
            return method(client, *args, **kwargs)

        if not client.credentials.refresh_expired():
            client.refresh()
            return method(client, *args, **kwargs)

        raise SessionExpiredError

    return wrapper


class SMTClient:
    """Basic client for interaction with the SMT API."""

    def __init__(
        self,
        username: str,
        password: str,
        *,
        smt_url: str = "https://am-pilot.sinergise.com/compute",
        token_url: str = "https://am-pilot.sinergise.com/auth/realms/am-pilot/protocol/openid-connect/token",
        client_id: str = "am-smt",
    ) -> None:
        """Initialize the client by acquiring access to SMT service using username and password."""
        self.smt_url = smt_url
        self.token_url = token_url
        self.client_id = client_id

        response = httpx.post(
            url=self.token_url,
            data={"client_id": self.client_id, "username": username, "password": password, "grant_type": "password"},
        )

        if response.status_code != 200:
            raise InvalidCredentialsError

        auth_rsp = AuthenticationResponse.parse_obj(response.json())
        self.credentials = UserCredentials(auth_response=auth_rsp)
        LOGGER.info(f"Logged in as user '{username}'.")

    def _get_auth_header(self) -> dict[str, str]:
        """Get the authorization header for the requests."""
        return {"Authorization": f"Bearer {self.credentials.access_token}"}

    def refresh(self) -> None:
        """Refresh the access token using the refresh token."""
        response = httpx.post(
            url=self.token_url,
            data={
                "client_id": self.client_id,
                "refresh_token": self.credentials.refresh_token,
                "grant_type": "refresh_token",
            },
        )

        if response.status_code != 200:
            raise TokenRefreshError

        auth_rsp = AuthenticationResponse.parse_obj(response.json())
        self.credentials = UserCredentials(auth_response=auth_rsp)
        LOGGER.info("Token refreshed.")

    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def api_version(self) -> str:
        """Version check of the SMT service."""
        response = httpx.request(method="GET", url=f"{self.smt_url}/version")

        response.raise_for_status()
        return response.content.decode()

    @token_required
    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def get_flow_run(self, flow_run_id: str) -> FlowRun:
        """Get the flow run status of the flow run with the matching ID provided by the user."""

        response = httpx.get(url=f"{self.smt_url}/flow-run/{flow_run_id}", headers=self._get_auth_header())

        response.raise_for_status()
        return FlowRun.parse_obj(response.json())

    @token_required
    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def create_and_configure_scope(self, params: ScopeConfigParams) -> FlowRun:
        """Triggers the 'General: 0 - Scope Creation and Configuration' deployment.

        Configure :class:`ScopeConfigParams` to create the scope and set up subscriptions. Choose a scope name in
        :class:`GeneralScopeConfig`. Enter AWS and SentinelHub account credentials in :class:`ResourceConfig`.
        Add single or multiple subscriptions per scope via :class:`SubscriptionsConfig`. Provide all available
        SentinelHub collections, both public or BYOC, for the scope via :class:`SentinelHubCollectionsConfig`.
        Optionally, codelists containing unique codes associated with certain crop or land-use types can be added
        using :class:`CodelistConfig`.


        You can read more about the configuration in the documentation of the :class:`ScopeConfigParams` class or in the
        `user-guide <https://gitext.sinergise.com/area-monitoring/community/-/blob/main/Signals&Markers%20Toolkit/user-manual/User-Manual.md#setting-up-a-scope>`_.

        Check `examples/basic-tutorial.ipynb` notebook for an example on how to configure and trigger this flow.
        """

        response = httpx.post(
            url=f"{self.smt_url}/setup-scope",
            content=params.json().encode("utf-8"),
            headers=self._get_auth_header(),
        )

        response.raise_for_status()
        return FlowRun.parse_obj(response.json())

    @token_required
    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def refdata_generation(self, params: RefdataFlowParams) -> FlowRun:
        """Triggers the 'General: 1 - Reference Data Ingest, Export and Transformation' deployment.

        This workflow is suitable when you want to inspect the reference data that is generated
        based on the provided geopackages without triggering signal download yet via :meth:`signal_download`. This can
        be prudent since signal download can be a time-consuming and resource intensive process and it makes sense
        to verify that it happens only when you are satisfied with other parts of the workflow.

        To run it, the scope and subscriptions must already be configured. See :meth:`create_and_configure_scope`.

        Configure :class:`RefdataFlowParams` to execute the creation of reference data. Set the `scope` and
        `iteration_id` via :class:`ComputationGeneralConfiguration`. Provide features of interest (FOIs)
        through the GeoPackage path and FOI type via the reference import configuration
        :class:`ReferenceImportConfiguration`. This can be either land use parcels (LU) or agricultural parcels (AP).

        SMT will create reference and geometry datasets based on the provided geopackages and all of the signal
        subscriptions that are available in the scope. The parquet datasets will be stored in the S3 bucket at
        the following locations:
            * `reference` - `s3://area-monitoring-<bucket-identifier>/<scope>/transformed-datasets/<iteration-id>/reference/<foi-type-code>/dataset/`
            * `geometry` - `s3://area-monitoring-<bucket-identifier>/<scope>/<subscription-code>/<iteration-id>/datasets/geometry/dataset/`

        The results of this flow can be re-used in :meth:`signal_download` or :meth:`smt_flow_run` if those are
        triggered with the same configuration that is common to the flows and more importantly,
        the same `iteration_id`.

        Check `examples/basic-tutorial.ipynb` notebook for an example on how to configure and trigger this flow.
        """

        response = httpx.post(
            url=f"{self.smt_url}/refdata",
            content=params.json().encode("utf-8"),
            headers=self._get_auth_header(),
        )

        response.raise_for_status()
        return FlowRun.parse_obj(response.json())

    @token_required
    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def signal_download(self, params: SignalDownloadFlowParams) -> FlowRun:
        """Triggers the General: 2 - Reference Data Ingest, Export, Transformation and Signal Download.

        This workflow is suitable when it is unclear which markers need to be calculated or if markers are not required.

        To run it, the scope and subscriptions must already be configured. See :meth:`create_and_configure_scope`.

        Configure :class:`SignalDownloadFlowParams` to execute the download. Set the `scope` and `iteration_id` via
        :class:`ComputationGeneralConfiguration`. Provide features of interest (FOIs) through the GeoPackage path and
        FOI type via the reference import configuration :class:`ReferenceImportConfiguration`. This can be either land
        use parcels (LU) or agricultural parcels (AP). Specify one or multiple signal download configurations
        :class:`SignalDownloadConfiguration`. Signal download happens iteratively only for FOIs and time-ranges
        not yet in the cache. Downloaded signal packages are stored on the S3 bucket as parquet datasets.

        Check `examples/basic-tutorial.ipynb` notebook for an example on how to configure and trigger this flow.

        """

        response = httpx.post(
            url=f"{self.smt_url}/signals",
            content=params.json().encode("utf-8"),
            headers=self._get_auth_header(),
        )

        response.raise_for_status()
        return FlowRun.parse_obj(response.json())

    @token_required
    @handle_http_status_errors(max_time=BACKOFF_MAX_TIME)
    def smt_flow_run(self, params: FullFlowParams) -> FlowRun:
        """Trigger 'General: 3 - Reference Data Ingest, Export, Transformation, Signal Download and Marker Computation'.

        To run it, the scope and subscriptions must already be configured. See :meth:`create_and_configure_scope`.

        Configure :class:`FullFlowParams` to execute the full flow. Set `scope` and `iteration_id` via
        :class:`ComputationGeneralConfiguration`. Provide features of interest (FOIs) through the GeoPackage path and
        FOI type via the reference import configuration :class:`ReferenceImportConfiguration`. This can be either land
        use parcels (LU) or agricultural parcels (AP). Specify one or multiple signal download configurations
        :class:`SignalDownloadConfiguration`. Signal download happens iteratively only for FOIs and time-ranges
        not yet in the cache. Downloaded signal packages are stored on the S3 bucket as parquet datasets. Specify
        marker computation configuration for specified signals via :class:`MarkerRunConfig`.

        Check `examples/basic-tutorial.ipynb` notebook for an example on how to configure and trigger this flow.
        """

        response = httpx.post(
            url=f"{self.smt_url}/markers",
            content=params.json().encode("utf-8"),
            headers=self._get_auth_header(),
        )

        response.raise_for_status()
        return FlowRun.parse_obj(response.json())
