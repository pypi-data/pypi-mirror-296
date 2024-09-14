"""This module contains Pydantic models that are needed to trigger one of the data generation workflows."""

from datetime import date

from pydantic import Field

from .base import SDKRequestBaseModel
from .markers.main import MarkersRunConfig


class ComputationGeneralConfiguration(SDKRequestBaseModel):
    """General information and configuration needed for computation."""

    scope: str = Field(
        description="ID/Name of the scope. Only upper-case letters, digits and underscores are supported.",
        title="Scope",
        regex=r"^[A-Z0-9_]+$",
    )
    iteration_id: str = Field(
        default="Iteration-1", description="ID of the iteration. Must be unique within the scope for a new iteration."
    )


class FoiTypeReferenceImportConfiguration(SDKRequestBaseModel):
    """Configuration for importing FOIs from a geopackage to the reference data service for a single FOI-type."""

    additionalAttributes: list[str] = Field(
        default_factory=list,
        description="A list of additional attributes that should be ingested from geopackage to reference data service",
        title="Additional Attributes",
        unique_items=True,
    )
    geoPackagePath: str = Field(
        description="Path of the geopackage on S3 for ingesting of FOIs into reference data service",
        title="GeoPackage Path",
    )
    tableName: str = Field(description="Layer of GeoPackage to be ingested", title="GeoPackage Table Name")


class ReferenceImportConfiguration(SDKRequestBaseModel):
    """Configuration for importing FOIs from a geopackage to the reference data service.
    Either agricultural parcels (AP) or land use parcels (LU) FOI configuration can be provided.
    """

    ap: FoiTypeReferenceImportConfiguration | None = Field(None, title="AP FOI Import Configuration")
    lu: FoiTypeReferenceImportConfiguration | None = Field(None, title="LU FOI Import Configuration")


class SignalPackageDownloadInputParams(SDKRequestBaseModel):
    """Input parameters for downloading signals associated with a specific subscription."""

    subscription_code: str = Field(
        description="Code of subscription for which signals should be downloaded", title="Signal Subscription Code"
    )
    intervalEnd: date | None = Field(
        description=(
            "The date until when the signals should be downloaded. If it is not provided it will be automatically "
            "deduced for each subscription based on the associated SentinelHub collection"
        ),
        title="Signal Interval End",
    )


class SignalDownloadConfiguration(SDKRequestBaseModel):
    """Configuration needed to download signals for one or multiple signal packages."""

    signal_package_downloads: list[SignalPackageDownloadInputParams] = Field(
        description="Signal Packages that should be created and signals downloaded for them.",
        title="Signal Packages",
        unique_items=True,
        min_items=1,
    )


class RefdataMixin(SDKRequestBaseModel):
    """Provides configuration for the Reference Data Ingest, Export and Transformation workflow."""

    general_configuration: ComputationGeneralConfiguration = Field(
        description="General configuration needed for computation", title="General Configuration"
    )
    foi_import_configuration: ReferenceImportConfiguration = Field(
        default_factory=ReferenceImportConfiguration,
        description=(
            "Configuration needed to import FOIs from a geopackage to the reference service. "
            "At least one of these, either for AP or LU FOIs, must be provided."
        ),
        title="Reference FOI Import Configuration",
    )


class SignalsMixin(SDKRequestBaseModel):
    """Provides configuration for the for the Signals Download workflow."""

    signal_download_configuration: SignalDownloadConfiguration = Field(
        description="Configuration needed to download signals for one or multiple signal packages.",
        title="Signal Download Configuration",
    )


class SMTMarkerRequestGenerationParams(SDKRequestBaseModel):
    """Marker request generation parameters specify the marker configuration and the environment of their
    calculation.
    """

    gitlab_project: str = Field(
        default="markers",
        description=(
            "Name of the associated GitLab project. "
            "Note: Should be left as 'markers' if the run requires is no other GitLab project containing custom "
            "computation logic."
        ),
        title="GitLab Project",
    )
    skip_publish: bool = Field(
        default=False,
        description="Boolean flag determining whether the publishing of calculated markers should be skipped.",
        title="Skip Markers publishing",
    )
    branch: str | None = Field(
        default=None,
        description=(
            "Name of the branch in `gitlab_project` repository used for marker calculation.  "
            "Note: Should be left blank if the user is unfamiliar with the concept of providing custom computation "
            "logic."
        ),
        title="GitLab Project Git Branch",
    )
    instance_types: list[str] | None = Field(
        default=None,
        description=(
            "List of AWS EC2 instance types that are used for calculation. The tooling chooses first available "
            "instance type from the list. Note: Should be left blank if user has no special preferences, the "
            "appropriate type is deduced in this case."
        ),
        title="EC2 Computation Instance Types",
    )
    markers_run_config: MarkersRunConfig = Field(
        default_factory=MarkersRunConfig,
        description=(
            "Run config for marker computation. Specifies the markers to be calculated and their configurations."
        ),
        title="Marker Computation Run Config",
    )


class MarkersMixin(SDKRequestBaseModel):
    """Mixin defining marker computation flow parameters."""

    marker_configuration: SMTMarkerRequestGenerationParams = Field(
        description="Marker computation parameters", title="Marker Computation Configuration"
    )


class RefdataFlowParams(RefdataMixin):
    """Input parameters for the refdata import/export flow."""


class SignalDownloadFlowParams(RefdataMixin, SignalsMixin):
    """Input parameters for the Reference Data Ingest, Export, Transformation and Signal Download."""


class FullFlowParams(RefdataMixin, SignalsMixin, MarkersMixin):
    """Input parameter for a full SMT flow.
    It consists of reference data ingestion, export, transformation, signal download and marker computation.
    """
