# pylint: disable=too-few-public-methods

"""Module for the Homogeneity standard marker configurations."""

from pydantic import Field, PositiveInt

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig


class S2L2AHomogeneity(BaseStandardMarkerConfig):
    """Configuration for the Homogeneity marker for S2L2A."""

    hm_thr: PositiveInt = Field(
        36,
        title="Homogeneity Threshold",
        description=(
            "The threshold compared to homogeneity hypothesis score to determine what the classification of a FOI is."
            "If score is larger than `hm_thr` than the `classification` is `homogeneous`, otherwise it is "
            "`heterogeneous`."
        ),
    )
    valid_query: str = Field(
        "(CLP <= 0.54 or CLM <= 0.99) and OUT_PROBA <= 0.5",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class PFHomogeneity(BaseStandardMarkerConfig):
    """Configuration for the Homogeneity marker for PF."""

    hm_thr: PositiveInt = Field(
        36,
        title="Homogeneity Threshold",
        description=(
            "The threshold compared to homogeneity hypothesis score to determine what the classification of a FOI is."
            "If score is larger than `hm_thr` than the `classification` is `homogeneous`, otherwise it is "
            "`heterogeneous`."
        ),
    )
    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=2",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class HomogeneityConfigs(BaseMarkerConfigs[S2L2AHomogeneity, PFHomogeneity]):
    """Configurations for the Homogeneity marker.

    The goal of homogeneity marker is to identify FOIs with multiple crops grown.
    """

    S2L2A: list[S2L2AHomogeneity] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFHomogeneity] = Field(default_factory=list, title="Source: PF")
