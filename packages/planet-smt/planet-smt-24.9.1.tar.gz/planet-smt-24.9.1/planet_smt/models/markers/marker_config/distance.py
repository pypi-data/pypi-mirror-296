# pylint: disable=too-few-public-methods

"""Module for the Distance standard marker configurations."""

from pydantic import Field

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig


class S2L2ADistance(BaseStandardMarkerConfig):
    """Configuration for the Distance marker for S2L2A."""

    label: str = Field(
        "CROP_LABEL", label="Label", description="Declaration of FOI class, used in neighbourhood FOI comparison."
    )
    valid_query: str = Field(
        "(CLP <= 0.54 or CLM <= 0.99) and OUT_PROBA <= 0.5",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )
    distance_time_intervals: str | None = Field(
        title="Distance Time Intervals",
        description=(
            "A parquet file where you can limit the distance calculation"
            " to a specific time interval for specific crop/land-use labels."
        ),
    )


class PFDistance(BaseStandardMarkerConfig):
    """Configuration for the Distance marker for PF."""

    label: str = Field(
        "CROP_LABEL", label="Label", description="Declaration of FOI class, used in neighbourhood FOI comparison."
    )
    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=2",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )
    distance_time_intervals: str | None = Field(
        title="Distance Time Intervals",
        description=(
            "A parquet file where you can limit the distance calculation"
            " to a specific time interval for specific crop/land-use labels."
        ),
    )


class DistanceConfigs(BaseMarkerConfigs[S2L2ADistance, PFDistance]):
    """Configurations for the Distance marker.

    It compares a FOI's NDVI time-series with other polygons time-series in its k=1 H3HEX neighbourhood.
    Final score is the median value of all compared euclidean distances.
    This is done for all hypotheses in the FOI's neighbourhood.
    """

    S2L2A: list[S2L2ADistance] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFDistance] = Field(default_factory=list, title="Source: PF")
