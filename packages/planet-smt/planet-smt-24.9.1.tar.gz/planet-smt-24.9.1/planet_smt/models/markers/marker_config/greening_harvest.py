# pylint: disable=too-few-public-methods

"""Module for the Greening/Harvest standard marker configurations."""

from pydantic import Field, NegativeFloat, NonNegativeFloat, PositiveFloat, PositiveInt

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig, WithRegionTimeFilter


class S2L2AGreeningHarvest(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Greening/Harvest marker for S2L2A."""

    greening_slope_thr: NegativeFloat = Field(
        -0.007,
        title="Greening Slope Threshold",
        description="Slope of time-series where we stop extending the event. Must be strictly less than zero.",
    )
    greening_delta_thr: PositiveFloat = Field(
        0.25,
        title="Greening Delta Threshold",
        description="Absolute measure that defines the magnitude of rise and fall in the NDVI time series "
        "required for an event to be valid. "
        "Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event.",
    )
    greening_drop_r: PositiveFloat = Field(
        0.20,
        title="Greening Drop Ratio",
        description="Relative measure in what the drop in the NDVI is required. "
        "In absolute terms it is calculated as `(delta_thr * drop_r)`.",
    )
    greening_grow_r: PositiveFloat = Field(
        0.60,
        title="Greening Grow Ratio",
        description="Relative measure in what the rise after a drop in NDVI is required. "
        "In absolute terms it is calculated as `(delta_thr * grow_r)`. "
        "Condition `END_VALUE > EXTREMA_VALUE + delta_thr * grow_r` must be satisfied for a valid event.",
    )
    greening_valley_to_peak_upper_bound: PositiveFloat = Field(
        0.19,
        title="Greening Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the peak of second event "
        "when merging two greening events.",
    )
    greening_valley_to_peak_time_bound: PositiveInt = Field(
        30,
        title="Greening Valley to Peak Time Bound",
        description="Upper bound for the time difference between the valley of first event and the peak of second "
        "event when merging two greening events.",
    )
    greening_valley_to_valley_upper_bound: PositiveFloat = Field(
        0.05,
        title="Greening Valley to Valley Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the valley of second event "
        "when merging two greening events.",
    )
    greening_valley_to_valley_time_bound: PositiveInt = Field(
        9999,
        title="Greening Valley to Valley Time Bound",
        description="Upper bound for the time difference between the first valley and the second valley when merging "
        "two greening events.",
    )
    greening_peak_to_peak_upper_bound: NonNegativeFloat = Field(
        0,
        title="Greening Peak to Peak Upper Bound",
        description="Upper bound of the jump/drop between the first and second peak of two consequent greening "
        "events.",
    )
    greening_peak_to_peak_time_bound: PositiveInt = Field(
        9999,
        title="Greening Peak to Peak Time Bound",
        description="Upper bound for the time difference between the first and second peak of two consequent "
        "greening events.",
    )
    greening_adjust_event_end_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Greening Adjust Event End Constraint Ratio",
        description="Option to control the adjustment of the event end. If set, the feature value of "
        "the new end will be constrained to be the set value * feature difference between "
        "original start and end from the original end feature value.",
    )
    greening_adjust_event_start_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Greening Adjust Event Start Constraint Ratio",
        description="Option to control the adjustment of the event start. If set, the feature value of "
        "the new start will be constrained to be the set value * feature difference between "
        "original start and end from the original start feature value.",
    )

    harvest_slope_thr: NegativeFloat = Field(
        -0.007,
        title="Harvest Slope Threshold",
        description="Slope of time-series where we stop extending the event. Must be strictly less than zero.",
    )
    harvest_delta_thr: PositiveFloat = Field(
        0.25,
        title="Harvest Delta Threshold",
        description="Absolute measure that defines the magnitude of rise and fall in the NDVI timeseries "
        "required for an event to be valid. "
        "Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event.",
    )
    harvest_drop_r: PositiveFloat = Field(
        0.20,
        title="Harvest Drop Ratio",
        description="Relative measure in what the drop in the time-series is required. "
        "In absolute terms it is calculated as `(delta_thr * drop_r)`.",
    )
    harvest_grow_r: PositiveFloat = Field(
        0.60,
        title="Harvest Grow Ratio",
        description="Relative measure in what the rise after a drop in the FEATURE is required. "
        "In absolute terms it is calculated as `(delta_thr * grow_r)`. "
        "Condition `END_VALUE > EXTREMA_VALUE + delta_thr * grow_r` must be satisfied for a valid event.",
    )
    harvest_valley_to_peak_upper_bound: PositiveFloat = Field(
        0.19,
        title="Harvest Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the peak of second event "
        "when merging two harvest events.",
    )
    harvest_valley_to_peak_time_bound: PositiveInt = Field(
        30,
        title="Harvest Valley to Peak Time Bound",
        description="Upper bound for the time difference between the valley of first event and the peak of second "
        "event when merging two harvest events.",
    )
    harvest_valley_to_valley_upper_bound: PositiveFloat = Field(
        0.05,
        title="Harvest Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the valley of second event "
        "when merging two harvest events.",
    )
    harvest_valley_to_valley_time_bound: PositiveInt = Field(
        9999,
        title="Harvest Valley to Valley Time Bound",
        description="Upper bound for the time difference between the first valley and the second valley when "
        "merging two harvest events.",
    )
    harvest_peak_to_peak_upper_bound: NonNegativeFloat = Field(
        0,
        title="Harvest Peak to Peak Upper Bound",
        description="Upper bound of the jump/drop between the first and second peak of two consequent harvest events.",
    )
    harvest_peak_to_peak_time_bound: PositiveInt = Field(
        9999,
        title="Harvest Peak to Peak Time Bound",
        description="Upper bound for the time difference between the first and second peak of two consequent harvest"
        " events.",
    )
    harvest_adjust_event_start_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Harvest Adjust Event Start Constraint Ratio",
        description="Option to control the adjustment of the event start. If set, the NDVI value "
        "of the new start will be constrained to be the set value * feature difference between original "
        "start and end from the original start feature value.",
    )
    harvest_adjust_event_end_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Harvest Adjust Event End Constraint Ratio",
        description="Option to control the adjustment of the event end. If set, the NDVI value "
        "of the new end will be constrained to be the set value * feature difference between original "
        "start and end from the original end feature value.",
    )

    bs_proba_thr: PositiveFloat = Field(
        0.9,
        title="Baresoil Threshold",
        description="Threshold of assignment of an observation as being bare-soil. Observations with pseudo-probability"
        " larger than this threshold are determined to be of bare-soil.",
    )
    valid_query: str = Field(
        "(CLP <= 0.99 or CLM <= 0.91) and OUT_PROBA <= 0.125",
        title="Valid Query",
        description="Definition of the filter used to determine valid observations.",
    )
    postprocess_queries: list[str] = Field(
        default_factory=list,
        title="Postprocessing Queries",
        unique_items=True,
        description=(
            "An optional list of queries. "
            "It lets user control false-positive detections by querying them as in Pandas query."
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


class PFGreeningHarvest(BaseStandardMarkerConfig, WithRegionTimeFilter):
    """Configuration for the Greening/Harvest marker for Planet Fusion."""

    greening_slope_thr: NegativeFloat = Field(
        -0.007,
        title="Greening Slope Threshold",
        description="Slope of time-series where we stop extending the event. Must be strictly less than zero.",
    )
    greening_delta_thr: PositiveFloat = Field(
        0.15,
        title="Greening Delta Threshold",
        description=(
            "Absolute measure that defines the magnitude of rise and fall in the NDVI "
            "required for an event to be valid. "
            "Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event."
        ),
    )
    greening_drop_r: PositiveFloat = Field(
        0.333,
        title="Greening Drop Ratio",
        description=(
            "Relative measure in what the drop in the time-series is required. "
            "In absolute terms it is calculated as `(delta_thr * drop_r)`."
        ),
    )
    greening_grow_r: PositiveFloat = Field(
        1,
        title="Greening Grow Ratio",
        description=(
            "Relative measure in what the rise after a drop in the FEATURE is required. "
            "In absolute terms it is calculated as `(delta_thr * grow_r)`. "
            "Condition `END_VALUE > EXTREMA_VALUE + delta_thr * grow_r` must be satisfied for a valid event."
        ),
    )
    greening_valley_to_peak_upper_bound: PositiveFloat = Field(
        0.11,
        title="Greening Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the peak of second event "
        "when merging two greening events.",
    )
    greening_valley_to_peak_time_bound: PositiveInt = Field(
        30,
        title="Greening Valley to Peak Time Bound",
        description="Upper bound for the time difference between the valley of first event and the peak of second "
        "event when merging two greening events.",
    )
    greening_valley_to_valley_upper_bound: PositiveFloat = Field(
        0.05,
        title="Greening Valley to Valley Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the valley of second event "
        "when merging two greening events.",
    )
    greening_valley_to_valley_time_bound: PositiveInt = Field(
        9999,
        title="Greening Valley to Valley Time Bound",
        description="Upper bound for the time difference between the first valley and the second valley when merging "
        "two greening events.",
    )
    greening_peak_to_peak_upper_bound: NonNegativeFloat = Field(
        0,
        title="Greening Peak to Peak Upper Bound",
        description="Upper bound of the jump/drop between the first and second peak of two consequent greening "
        "events.",
    )
    greening_peak_to_peak_time_bound: PositiveInt = Field(
        9999,
        title="Greening Peak to Peak Time Bound",
        description="Upper bound for the time difference between the first and second peak of two consequent "
        "greening events.",
    )
    greening_adjust_event_end_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Greening Adjust Event End Constraint Ratio",
        description=(
            "Option to control the adjustment of the event end. If set, the feature value "
            "of the new end will be constrained to be the set value * feature difference between original start"
            " and end from the original end feature value."
        ),
    )
    greening_adjust_event_start_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Greening Adjust Event Start Constraint Ratio",
        description=(
            "Option to control the adjustment of the event start. If set, the feature value "
            "of the new start will be constrained to be the set value * feature difference between original start"
            " and end from the original start feature value."
        ),
    )

    harvest_slope_thr: NegativeFloat = Field(
        -0.007,
        title="Harvest Slope Threshold",
        description="Slope of time-series where we stop extending the event. Must be strictly less than zero.",
    )
    harvest_delta_thr: PositiveFloat = Field(
        0.15,
        title="Harvest Delta Threshold",
        description=(
            "Absolute measure that defines the magnitude of rise and fall in the FEATURE "
            "required for an event to be valid. "
            "Condition `abs(START_VALUE - EXTREMA_VALUE) >= delta_thr` must be satisfied for a valid event."
        ),
    )
    harvest_drop_r: PositiveFloat = Field(
        0.333,
        title="Harvest Drop Ratio",
        description=(
            "Relative measure in what the drop in the time-series is required. "
            "In absolute terms it is calculated as `(delta_thr * drop_r)`."
        ),
    )
    harvest_grow_r: PositiveFloat = Field(
        1,
        title="Harvest Grow Ratio",
        description=(
            "Relative measure in what the rise after a drop in the FEATURE is required. "
            "In absolute terms it is calculated as `(delta_thr * grow_r)`. "
            "Condition `END_VALUE > EXTREMA_VALUE + delta_thr * grow_r` must be satisfied for a valid event."
        ),
    )
    harvest_valley_to_peak_upper_bound: PositiveFloat = Field(
        0.11,
        title="Harvest Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the peak of second event "
        "when merging two harvest events.",
    )
    harvest_valley_to_peak_time_bound: PositiveInt = Field(
        30,
        title="Harvest Valley to Peak Time Bound",
        description="Upper bound for the time difference between the valley of first event and the peak of second "
        "event when merging two harvest events.",
    )
    harvest_valley_to_valley_upper_bound: PositiveFloat = Field(
        0.05,
        title="Harvest Valley to Peak Upper Bound",
        description="Upper bound for the jump/drop between the valley of first event and the valley of second event "
        "when merging two harvest events.",
    )
    harvest_valley_to_valley_time_bound: PositiveInt = Field(
        9999,
        title="Harvest Valley to Valley Time Bound",
        description="Upper bound for the time difference between the first valley and the second valley when "
        "merging two harvest events.",
    )
    harvest_peak_to_peak_upper_bound: NonNegativeFloat = Field(
        0,
        title="Harvest Peak to Peak Upper Bound",
        description="Upper bound of the jump/drop between the first and second peak of two consequent harvest events.",
    )
    harvest_peak_to_peak_time_bound: PositiveInt = Field(
        9999,
        title="Harvest Peak to Peak Time Bound",
        description="Upper bound for the time difference between the first and second peak of two consequent harvest"
        " events.",
    )
    harvest_adjust_event_end_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Harvest Adjust Event End Constraint Ratio",
        description=(
            "Option to control the adjustment of the event end. "
            "If set, the feature value of the new end will be constrained to be the set value * "
            "feature difference between original start and end from the original end feature value."
        ),
    )
    harvest_adjust_event_start_constraint_ratio: PositiveFloat = Field(
        0.20,
        title="Harvest Adjust Event Start Constraint Ratio",
        description=(
            "Option to control the adjustment of the event start. "
            "If set, the feature value of the new start will be constrained to be the set value * feature difference "
            "between original start and end from the original start feature value."
        ),
    )

    bs_proba_thr: PositiveFloat = Field(
        0.65,
        title="Baresoil Threshold",
        description=(
            "Threshold of assignment of an observation as being bare-soil. Observations with pseudo-probability larger "
            "than this threshold are determined to be of bare-soil."
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


class GreeningHarvestConfigs(BaseMarkerConfigs[S2L2AGreeningHarvest, PFGreeningHarvest]):
    """Configurations for the Greening/Harvest marker.

    The Greening and Harvest marker can be separately customised for the two types of events
    (greening events and harvest events).
    """

    S2L2A: list[S2L2AGreeningHarvest] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFGreeningHarvest] = Field(default_factory=list, title="Source: PF")
