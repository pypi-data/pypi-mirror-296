"""This module contains Pydantic models for the input parameters of the AM Orchestrator flows."""

from datetime import date
from typing import Any, Literal, Self

from pydantic import Field, root_validator, validator

from .base import SDKRequestBaseModel, SDKRequestCredentials, SDKResponseBaseModel


class InputCode(SDKRequestBaseModel):
    """Model for a code that can be added to a scope. The `code` field is the internal Area Monitoring identifier."""

    code: str = Field(description="Unique code associated with a certain crop/land-use type.", title="Code")
    names: dict[str, str] | None = Field(
        None, description="Human-readable names of the code supporting localization.", title="Names"
    )


class SentinelHubCredentials(SDKRequestCredentials):
    """SentinelHub credentials tied to your SentinelHub subscriptions."""

    clientId: str = Field(title="Client ID")
    clientSecret: str = Field(title="Client Secret")

    def to_request_dict(self) -> dict[str, str]:
        """Returns the credentials as a dictionary suitable for a request."""
        return {**self.dict(), "type": "SENTINEL_HUB"}


PublicSentinelHubCollectionCodes = Literal["S1GRDA", "S1GRDD", "S2L1C", "S2L2A", "S2SR"]
ByocSentileHubCollectionCodes = Literal["S2SR", "ARPS", "PF", "S1COH"]
SentinelHubCollectionCodes = Literal["S1GRDA", "S1GRDD", "S2L1C", "S2L2A", "S2SR", "S2SR", "ARPS", "PF", "S1COH"]


class GeneralScopeConfig(SDKRequestBaseModel):
    """Model for the general configuration of a scope."""

    scope: str = Field(
        description="ID/Name of the scope. Only upper-case letters, digits and underscores are supported.",
        title="Scope",
        regex=r"^[A-Z0-9_]+$",
    )
    srid: int = Field(
        description=(
            "Enter EPSG code of the SRID projection of the geometries in the geopackage you will provide. "
            "Must be a metric SRID. See list of supported ones here: https://epsg.io."
        ),
        title="SRID",
    )


class BaseResourceConfig(SDKRequestBaseModel):
    """Base model for the configuration of resources needed for a scope."""

    reuse_from_scope: str | None = Field(
        None,
        description="Scope identifier from which the credentials and resources should be reused",
        title="Reuse from Scope ID",
    )


class AwsResourceConfig(BaseResourceConfig):
    """Model for the configuration of AWS resources needed for a scope."""

    bucket_identifier: str = Field(
        description=(
            "Identifier of the bucket in the case when a new bucket needs to be created."
            " Can only contain lower case letters and hyphens."
            " An associated bucket named `s3://area-monitoring-{bucket-identifier}` will be created."
        ),
        regex=r"^[a-z\-]+$",
    )


class ShResourceConfig(BaseResourceConfig):
    """Model for the configuration of SentinelHub credentials needed for a scope."""

    credentials: SentinelHubCredentials | None = Field(None, title="SentinelHub Credentials")

    @root_validator
    @classmethod
    def verify_root_model(cls, model: dict[str, Any] | SDKRequestBaseModel) -> dict[str, Any] | SDKRequestBaseModel:
        """Checks that either credentials are specified or a scope is specified from which to reuse credentials."""

        if isinstance(model, SDKRequestBaseModel):
            model = model.dict()

        if model["credentials"] is None and model["reuse_from_scope"] is None:
            raise ValueError("At least one SH collection source must be specified.")

        return model


class ResourceConfig(SDKRequestBaseModel):
    """Model for the configuration of all resources needed for a scope."""

    sh_configuration: ShResourceConfig = Field(
        description="SentinelHub account-related configuration",
        title="SentinelHub Configuration",
    )
    aws_configuration: AwsResourceConfig = Field(
        description="Inputs needed to set-up AWS access. If a scope for reuse is provided this will take priority",
        title="AWS Configuration",
    )


class CodelistConfig(SDKRequestBaseModel):
    """Model for the configuration of codelists to add to a scope."""

    crop_codes: list[InputCode] = Field(
        default_factory=list, description="List of crop codes to add to scope.", unique_items=True
    )
    land_use_codes: list[InputCode] = Field(
        default_factory=list, description="List of land-use codes to add to scope.", unique_items=True
    )

    @validator("crop_codes", "land_use_codes", pre=False)
    @classmethod
    def check_codelist_uniqueness(cls, codes: list[InputCode]) -> list[InputCode]:
        """Check that each entry in a codelist has a unique 'code' field."""

        if len(codes) != len({code.code for code in codes}):
            raise ValueError("Each entry in a codelist must have a unique 'code', however some are duplicated.")

        return codes


class PublicSHCollection(SDKRequestBaseModel):
    """Model for a public SentinelHub collection that you want to add to the scope. The `sh_collection_source` field
    is automatically set based on the code field. The `code` is a internal Area Monitoring identifier,
    while the source is the SentinelHub identifier. Since this is a public collection, its source is well known.
    """

    code: PublicSentinelHubCollectionCodes = Field(description="Code of the collection", title="Collection Code")

    @property
    def sh_collection_source(self) -> str:
        """Return the SentinelHub public source identifier of the collection based on the code."""

        if self.code == "S1GRDA":
            return "sentinel-1-grd"

        if self.code == "S1GRDD":
            return "sentinel-1-grd"

        if self.code == "S2L1C":
            return "sentinel-2-l1c"

        return "sentinel-2-l2a"


class BYOCSHCollection(SDKRequestBaseModel):
    """Model for a BYOC SentinelHub collection that you want to add to the scope. In contrast to `PublicSHCollection`s,
    the `sh_collection_source` field is defined when the data is ingested as a BYOC, thefore it must be provided.
    """

    code: ByocSentileHubCollectionCodes = Field(description="Code of the collection", title="Collection Code")
    sh_collection_source: str = Field(description="Source of the collection", title="Collection Source")


class SentinelHubCollectionsConfig(SDKRequestBaseModel):
    """Model for the configuration of SentinelHub collections that you want to add to the scope."""

    public_sh_collections: list[PublicSHCollection] = Field(
        default_factory=list,
        description="Public SentinelHub collections that you want available to the scope.",
        title="Public SentinelHub Collections",
        unique_items=True,
    )
    byoc_sh_collection: list[BYOCSHCollection] = Field(
        default_factory=list,
        description="BYOC SentinelHub collections that you want available to the scope.",
        title="BYOC SentinelHub Collections",
    )

    @root_validator
    @classmethod
    def verify_root_model(cls, model: dict[str, Any] | SDKRequestBaseModel) -> dict[str, Any] | SDKRequestBaseModel:
        """Checks that the configuration is valid by making sure at least one public or BYOC collection is specified."""

        if isinstance(model, SDKRequestBaseModel):
            model = model.dict()

        # at least one public or BYOC collection must be specified for the scope
        if len(model["public_sh_collections"]) == 0 and len(model["byoc_sh_collection"]) == 0:
            raise ValueError("At least on SH collection source must be specified.")

        # check that each BYOC collection has a unique code so that we aren't specifying the same data type twice
        # for public collections this check is done for us by Pydantic as we see 'unique_items=True'
        # in the field definition
        byoc_collections: list[dict[str, Any] | SDKRequestBaseModel] = model["byoc_sh_collection"]

        unique_codes = set()
        for collection in byoc_collections:
            if isinstance(collection, SDKRequestBaseModel):
                collection = collection.dict()

            if collection["code"] in unique_codes:
                raise ValueError(
                    "Each BYOC collection must have a unique 'Collection Code', however some are duplicated."
                )

            unique_codes.add(collection["code"])

        return model


class SubscriptionConfig(SDKResponseBaseModel):
    """Configuration for Signal Subscriptions. Subscriptions are defined by a time-interval of interest, a SentinelHub
    collection as a source of data, and a set of features-of-interest (FOIs) through a filter on reference data.
    They can then be triggered to create signals for the at will to create signal data in an
    iterative and efficient manner.

    You can read more details about their setup in the `user-guide <https://gitext.sinergise.com/area-monitoring/community/-/blob/main/Signals&Markers%20Toolkit/user-manual/User-Manual.md#subscription-configuration>`_.
    """

    code: str = Field(
        description=(
            "Unique code associated with the subscription. "
            "It is referenced in subsequent flows to associate signal creation with a specific subscription."
        ),
        title="Code",
    )
    intervalStart: date = Field(description="Earliest date included in signal creation.", title="Interval Start")
    intervalEnd: date = Field(description="Latest date that can be included in signal creation.", title="Interval End")
    shCollectionCode: SentinelHubCollectionCodes = Field(
        description="Short-hand code for the source of signals data.", title="Collection Code"
    )
    foiFilter: str | None = Field(
        description="Query to filter FOIs based on the associated reference data.",
        title="FOI Query",
    )
    foiTypeCode: Literal["AP", "LU"] = Field(
        description="Type of FOI to filter on. AP/LU for Agricultural/Land User Parcels respectively.", title="FOI Type"
    )

    @validator("code")
    @classmethod
    def check_code_validity(cls, value: str) -> str:
        """Checks if the subscription code is valid."""
        if "." in value or "-" in value:
            raise ValueError("Subscription code must not contain dots or hyphens.")
        return value

    @root_validator
    @classmethod
    def verify_root_model(cls, model: dict[str, Any] | SDKRequestBaseModel) -> dict[str, Any] | SDKRequestBaseModel:
        """Validates the root model by making sure that the intervalEnd is strictly greater than intervalStart."""
        if isinstance(model, SDKRequestBaseModel):
            model = model.dict()

        start_date = model["intervalStart"]
        if not isinstance(start_date, date):
            start_date = date.fromisoformat(start_date)

        end_date = model["intervalEnd"]
        if not isinstance(end_date, date):
            end_date = date.fromisoformat(end_date)

        if end_date <= start_date:
            raise ValueError("End date must be stricly greater than start date")

        return model


class SubscriptionsConfig(SDKRequestBaseModel):
    """Model for the configuration of subscriptions to create for a scope.

    Can specify multiple subscriptions that can share time-of-interest, source of data, and FOI filter.
    """

    subscriptions: list[SubscriptionConfig] = Field(
        description="List of subscriptions to create.", min_items=1, unique_items=True
    )


class ScopeConfigParams(SDKRequestBaseModel):
    """Configuration parameters to setup a scope with desired SentinelHub collections,
    credentials to access them, create AWS resources, etc.
    """

    general_configuration: GeneralScopeConfig = Field(description="General configuration of the scope.")
    resource_configuration: ResourceConfig = Field(
        description="Resources tied to scope like SentinelHub and AWS configurations."
    )
    codelist_configuration: CodelistConfig = Field(
        default_factory=CodelistConfig, description="Codelists to add to scope."
    )
    sentinel_hub_collections_configuration: SentinelHubCollectionsConfig = Field(
        description="SentinelHub collections to add to scope."
    )
    subscription_configuration: SubscriptionsConfig = Field(description="Signal Subscriptions to add to scope.")

    @root_validator
    @classmethod
    def verify_root_model(cls, model: dict[str, Any] | Self) -> dict[str, Any] | Self:
        """Checks that the SentinelHub collections specified in the subscriptions
        are configured to be added to the scope.
        """

        if isinstance(model, dict):
            sub_config = SubscriptionsConfig.validate(model["subscription_configuration"])
            sentinel_hub_collections_configuration = SentinelHubCollectionsConfig.validate(
                model["sentinel_hub_collections_configuration"]
            )
        else:
            sub_config = model.subscription_configuration
            sentinel_hub_collections_configuration = model.sentinel_hub_collections_configuration

        subscription_sources = {subscription.shCollectionCode for subscription in sub_config.subscriptions}

        scope_sources = {
            collection.code for collection in sentinel_hub_collections_configuration.byoc_sh_collection
        } | {collection.code for collection in sentinel_hub_collections_configuration.public_sh_collections}

        # check that the sources used in the subscriptions are available in the scope
        missing_sources = subscription_sources - scope_sources
        if len(missing_sources) > 0:
            raise ValueError(
                "The desired subscriptions want to use the sources, however "
                "they were not chosen as a SentinelHub collection to be added to the scope."
            )

        return model
