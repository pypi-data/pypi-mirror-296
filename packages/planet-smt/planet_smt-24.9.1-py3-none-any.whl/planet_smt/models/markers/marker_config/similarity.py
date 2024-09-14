# pylint: disable=too-few-public-methods

"""Module for the Similarity standard marker configurations."""

from pydantic import Field

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig


class S2L2ASimilarity(BaseStandardMarkerConfig):
    """Configuration for the Similarity marker for S2L2A."""

    label: str = Field(
        "CROP_LABEL", title="Label", description="Type declaration to use to compare FOI with neighbourhood FOIs."
    )
    valid_query: str = Field(
        "(CLP <= 0.54 or CLM <= 0.99) and OUT_PROBA <= 0.5",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class PFSimilarity(BaseStandardMarkerConfig):
    """Configuration for the Similarity marker for PF."""

    label: str = Field(
        "CROP_LABEL", title="Label", description="Type declaration to use to compare FOI with neighbourhood FOIs."
    )
    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=2",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class SimilarityConfigs(BaseMarkerConfigs[S2L2ASimilarity, PFSimilarity]):
    """Configurations for the Similarity marker.

    The marker compares a FOIs time-series desired FEATURE (usually 'NDVI') to it's meanhood for all LABEL's in
    it's k=1 neighbourhood. Based on this comparsion it outputs a chi-squared score value for each hypothesis.
    """

    S2L2A: list[S2L2ASimilarity] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFSimilarity] = Field(default_factory=list, title="Source: PF")
