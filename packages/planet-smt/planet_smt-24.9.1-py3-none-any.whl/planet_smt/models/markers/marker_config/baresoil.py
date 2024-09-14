# pylint: disable=too-few-public-methods

"""Module for the Baresoil standard marker configurations."""

from pydantic import Field, PositiveFloat

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig, WithRegionTimeFilter


class S2L2ABaresoil(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Baresoil marker for S2L2A."""

    bs_proba_thr: PositiveFloat = Field(0.9, title="Baresoil Threshold")
    valid_query: str = Field(
        "(CLP <= 0.54 or CLM <= 0.99) and OUT_PROBA <= 0.5",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )

    summary_crop_ids: list[str] | None = Field(
        title="Summary Crop IDs",
        description=(
            "An optional list of crop codes for subsetting a marker calculation report. "
            "If omitted, all the crops are regarded as relevant."
        ),
        unique_items=True,
    )


class PFBaresoil(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Baresoil marker for PF."""

    bs_proba_thr: PositiveFloat = Field(0.65, title="Baresoil Threshold")
    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=2",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )

    summary_crop_ids: list[str] | None = Field(
        title="Summary Crop IDs",
        unique_items=True,
        description=(
            "An optional list of crop codes for subsetting a marker calculation report. "
            "If omitted, all the crops are regarded as relevant."
        ),
    )


class BaresoilConfigs(BaseMarkerConfigs[S2L2ABaresoil, PFBaresoil]):
    """Configurations for the Baresoil marker.
    The Baresoil marker is used to identify which observations of a FOI are that of bare-soil.
    """

    S2L2A: list[S2L2ABaresoil] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFBaresoil] = Field(default_factory=list, title="Source: PF")
