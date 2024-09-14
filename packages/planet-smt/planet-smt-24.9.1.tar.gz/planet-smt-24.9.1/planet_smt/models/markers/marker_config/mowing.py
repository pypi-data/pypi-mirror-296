# pylint: disable=too-few-public-methods

"""Module for the Mowing standard marker configurations."""

from pydantic import Field, NegativeFloat, PositiveFloat

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig, WithRegionTimeFilter


class S2L2AMowing(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Mowing marker for S2L2A."""

    slope_thr: NegativeFloat = Field(
        -0.007,
        title="Slope Threshold",
        description="Slope of NDVI where we stop extending the event. Must be strictly less than zero",
    )
    delta_thr: PositiveFloat = Field(
        0.11,
        title="Delta Threshold",
        description=(
            "Absolute measure that defines the magnitude of rise and fall in NDVI required for an event to be valid. "
            "Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event."
        ),
    )
    drop_r: PositiveFloat = Field(
        0.5,
        title="Drop Ratio",
        description=(
            "Relative measure in what the drop in the NDVI is required. "
            "In absolute terms it is calculated as `(delta_thr * drop_r)`."
        ),
    )
    grow_r: PositiveFloat = Field(
        0.8,
        title="Grow Ratio",
        description=(
            "Relative measure in what the rise after a drop in the NDVI is required. "
            "In absolute terms it is calculated as (delta_thr * grow_r). "
            "Condition END_VALUE > EXTREMA_VALUE + delta_thr * grow_r must be satisfied for a valid event."
        ),
    )
    valley_to_peak_upper_bound: PositiveFloat = Field(
        0.088,
        title="Valley to Peak Upper Bound",
        description=(
            "Upper bound for the jump/drop between the first valley and the second peak of a consequent rise "
            "and fall pair can have in order to be merged."
        ),
    )
    adjust_event_end_constraint_ratio: PositiveFloat | None = Field(
        None,
        title="Adjust Event End Constraint Ratio",
        description=(
            "Option to control the adjustment of the event start. "
            "If set, the feature value of the new start will be constrained to be the set value * feature difference "
            "between original start and end from the original start feature value."
        ),
    )
    adjust_event_start_constraint_ratio: PositiveFloat | None = Field(
        None,
        title="Adjust Event Start Constraint Ratio",
        description=(
            "Option to control the adjustment of the event end. "
            "If set, the feature value of the new end will be constrained to be the set value * feature difference "
            "between original start and end from the original end feature value."
        ),
    )
    valid_query: str = Field(
        "CLP <= 0.4 and OUT_PROBA <= 0.8",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )
    postprocess_queries: list[str] = Field(
        default_factory=list,
        title="Postprocessing Queries",
        unique_items=True,
        description=(
            "An optional list of queries. It lets user control false-positive detections by querying them as in Pandas "
            "query."
        ),
    )
    summary_crop_ids: list[str] | None = Field(
        title="Summary Crop IDs",
        unique_items=True,
        description=(
            "An optional list of crop codes for subsetting a marker calculation report. "
            "If omitted, all the crops are regarded as relevant."
        ),
    )


class PFMowing(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Mowing marker for PF."""

    slope_thr: NegativeFloat = Field(
        -0.00018,
        title="Slope Threshold",
        description="Slope of NDVI where we stop extending the event. Must be strictly less than zero",
    )
    delta_thr: PositiveFloat = Field(
        0.06,
        title="Delta Threshold",
        description=(
            "Absolute measure that defines the magnitude of rise and fall in the FEATURE required for an event to be "
            "valid. Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event."
        ),
    )
    drop_r: PositiveFloat = Field(
        0.5,
        title="Drop Ratio",
        description=(
            "Relative measure in what the drop in the FEATURE is required. "
            "In absolute terms it is calculated as `(delta_thr * drop_r)`."
        ),
    )
    grow_r: PositiveFloat = Field(
        1.2,
        title="Grow Ratio",
        description=(
            "Relative measure in what the rise after a drop in the FEATURE is required. "
            "In absolute terms it is calculated as (delta_thr * grow_r). "
            "Condition END_VALUE > EXTREMA_VALUE + delta_thr * grow_r must be satisfied for a valid event."
        ),
    )
    valley_to_peak_upper_bound: PositiveFloat = Field(
        0.072,
        title="Valley to Peak Upper Bound",
        description=(
            "Upper bound for the jump/drop between the first valley and the second peak of a consequent rise and fall "
            "pair can have in order to be merged."
        ),
    )
    adjust_event_end_constraint_ratio: PositiveFloat | None = Field(
        None,
        title="Adjust Event End Constraint Ratio",
        description=(
            "Option to control the adjustment of the event start. "
            "If set, the feature value of the new start will be constrained to be the set value * feature difference "
            "between original start and end from the original start feature value."
        ),
    )
    adjust_event_start_constraint_ratio: PositiveFloat | None = Field(
        None,
        title="Adjust Event Start Constraint Ratio",
        description=(
            "Option to control the adjustment of the event end. "
            "If set, the feature value of the new end will be constrained to be the set value * feature difference "
            "between original start and end from the original end feature value."
        ),
    )
    valid_query: str = Field(
        "abs(DAYS_TO_NEAREST_OBS)<=1",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )
    postprocess_queries: list[str] = Field(
        default_factory=list,
        title="Postprocessing Queries",
        unique_items=True,
        description=(
            "An optional list of queries. It lets user control false-positive detections by querying them as in Pandas "
            "query."
        ),
    )
    summary_crop_ids: list[str] | None = Field(
        title="Summary Crop IDs",
        unique_items=True,
        description=(
            "An optional list of crop codes for subsetting a marker calculation report. "
            "If omitted, all the crops are regarded as relevant."
        ),
    )


class MowingConfigs(BaseMarkerConfigs[S2L2AMowing, PFMowing]):
    """Configurations for the Mowing marker."""

    S2L2A: list[S2L2AMowing] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFMowing] = Field(default_factory=list, title="Source: PF")
