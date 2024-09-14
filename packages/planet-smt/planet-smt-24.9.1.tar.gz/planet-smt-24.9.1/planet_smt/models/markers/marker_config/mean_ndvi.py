# pylint: disable=too-few-public-methods

"""Module for the MeanNdvi standard marker configurations."""

from datetime import date

from pydantic import Field, validator

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig
from .utils import validate_start_and_end_date_consistency


class BaseMeanNdvi(BaseStandardMarkerConfig):
    """Base class for NDVI configurations."""

    aggregation_start_date: date = Field(
        title="Aggregation Start Date", description="The start date of NDVI aggregation period in format 'YYYY-MM-DD'."
    )
    aggregation_end_date: date = Field(
        title="Aggregation End Date", description="The end date of NDVI aggregation period in format 'YYYY-MM-DD'."
    )

    summary_crop_ids: list[str] | None = Field(
        title="Summary Crop IDs",
        unique_items=True,
        description=(
            "An optional list of crop codes for subsetting a marker calculation report. "
            "If omitted, all the crops are regarded as relevant."
        ),
    )

    @validator("aggregation_start_date", pre=True, allow_reuse=True)
    @classmethod
    def parse_start_date(cls, v: object) -> object:
        """Parse the start date from a string to a date object."""
        return date.fromisoformat(v) if isinstance(v, str) else v

    @validator("aggregation_end_date", pre=True, allow_reuse=True)
    @classmethod
    def parse_end_date(cls, v: object) -> object:
        """Parse the end date from a string to a date object."""
        return date.fromisoformat(v) if isinstance(v, str) else v

    @validator("aggregation_end_date", allow_reuse=True)
    @classmethod
    def validate_end_date(cls, v: date, values: dict[str, str | date]) -> str | date:
        """Validate the end date is after the start date."""
        start_date = values["aggregation_start_date"]
        validate_start_and_end_date_consistency(start_date=start_date, end_date=v)
        return v


class S2L2AMeanNdvi(BaseMeanNdvi):
    """Configuration for the S2L2A NDVI marker."""

    valid_query: str = Field(
        "(CLP <= 0.54 or CLM <= 0.99) and OUT_PROBA <= 0.5",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class PFMeanNdvi(BaseMeanNdvi):
    """Configuration for the PF NDVI marker."""

    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=2",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )


class MeanNdviConfigs(BaseMarkerConfigs[S2L2AMeanNdvi, PFMeanNdvi]):
    """Configurations for the Mean NDVI marker.

    The result is the mean NDVI value for each FOI in the aggregation period.
    """

    S2L2A: list[S2L2AMeanNdvi] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFMeanNdvi] = Field(default_factory=list, title="Source: PF")
