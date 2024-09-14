# pylint: disable=too-few-public-methods

"""Module for the the common parts of every standard marker configuration."""

from typing import Any, Generic, Self, TypeVar

from pydantic import Field, validator
from pydantic.generics import GenericModel

from ...base import SDKRequestBaseModel


class BaseStandardMarkerConfig(SDKRequestBaseModel):
    """Base class for standard marker configurations.

    Each marker configuration has a subscription name and an identifier suffix.
    Such parametrization allows for the user to specify multiple markers of the same type and source
    and distinguish between them with `identifier_suffix`.

    WARNING: If a single marker config for a certain source and a type of a marker is provided,
    then `identifier_suffix` can be left empty.
    However if multiple are provided, user must ensure that marker configs of the same source and type of marker do not
    share the same `identifier_suffix` or the validation will fail.
    One can still be left blank, but the others of the same source and type must have the `identifier_suffix` defined.
    """

    identifier_suffix: str = Field(
        default="",
        title="Identifier Suffix",
        description=(
            "A suffix added to a marker to distinguish it from other markers that have the same type and "
            "source. It defaults to an empty string if not provided."
        ),
    )
    subscription_name: str = Field(
        title="Subscription Name",
        description="Subscription code associated with the signal package user wants to run the marker on.",
    )
    foi_selector_query: str | None = Field(
        title="FOI Selector Query",
        description=(
            "A reference dataset-based pandas query to define which FOIs "
            "to include in the computation of the corresponding standard marker."
        ),
    )


class WithRegionTimeFilter(SDKRequestBaseModel):
    """Mixin for marker configurations that defines a region time filter.
    Time filter is a parquet dataset containing set of large polygons with associated temporal filters.
    For each of these filtering polygons all intersecting FOI polygons have invalidated their observations
    within the filtering interval.
    """

    region_time_filter: str | None = Field(
        title="Region Time Validity Filter",
        description=(
            "Path to a Parquet dataset on SMT-accessible S3 bucket containing set of large polygons with "
            "associated temporal filters."
        ),
    )


U = TypeVar("U", bound=BaseStandardMarkerConfig)
V = TypeVar("V", bound=BaseStandardMarkerConfig)


class BaseMarkerConfigs(GenericModel, Generic[U, V]):
    """Base class for marker configurations."""

    S2L2A: list[U] = Field(
        default_factory=list, title="Source: S2L2A", description="Marker configurations for S2L2A-based subscriptions."
    )
    PF: list[V] = Field(
        default_factory=list, title="Source: PF", description="Marker configurations for PF-based subscriptions."
    )

    @validator("S2L2A", "PF")
    @classmethod
    def validate_marker_configs_are_not_duplicated(
        cls,
        marker_configs: list[U | V],
    ) -> list[U | V]:
        """Ensure that there are no duplicated marker configurations."""

        if len(marker_configs) == 0:
            return marker_configs

        unique_combos = set()
        non_unique_combos: set[U | V] = set()
        for marker_config in marker_configs:
            if marker_config.identifier_suffix in unique_combos:
                non_unique_combos.add(marker_config)
                continue

            unique_combos.add(marker_config.identifier_suffix)

        if not non_unique_combos:
            return marker_configs

        error = (
            "Only one marker per (source, type, identifier_suffix) combination is supported, "
            "however some are duplicated:\n"
        )
        for marker_config in non_unique_combos:
            error += f"  - {marker_config.json(indent=4)})\n"

        raise ValueError(error)

    @property
    def subscriptions(self) -> set[str]:
        """Return the set of subscriptions that are used in the marker configurations."""

        return {model.subscription_name for model in self.S2L2A} | {model.subscription_name for model in self.PF}

    @classmethod
    def combine(cls, left: Any, right: Any) -> Self:
        """Combine two marker configurations, by taking the all right ones and only adding ones
        from left that are not present in right. Presence/Equality in this context is determined
        by the identifier_suffix attribute.
        """

        if not isinstance(left, cls):
            raise ValueError(f"Cannot use combine of '{cls.__name__}' with '{type(left)}'.")

        if not isinstance(right, cls):
            raise ValueError(f"Cannot use combine of '{cls.__name__}' with '{type(right)}'.")

        s2l2a_identifiers = {marker.identifier_suffix for marker in left.S2L2A}
        pf_identifiers = {marker.identifier_suffix for marker in left.PF}

        s2l2a = left.S2L2A + [
            right_marker for right_marker in right.S2L2A if right_marker.identifier_suffix not in s2l2a_identifiers
        ]
        pf = left.PF + [
            right_marker for right_marker in right.PF if right_marker.identifier_suffix not in pf_identifiers
        ]

        return cls(S2L2A=s2l2a, PF=pf)
