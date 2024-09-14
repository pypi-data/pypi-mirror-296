"""A module for the marker configurations and execution request models."""

from typing import Any, Self

from pydantic import Field

from ..base import SDKRequestBaseModel
from .marker_config.baresoil import BaresoilConfigs
from .marker_config.classification import ClassificationConfigs
from .marker_config.distance import DistanceConfigs
from .marker_config.greening_harvest import GreeningHarvestConfigs
from .marker_config.homogeneity import HomogeneityConfigs
from .marker_config.mean_ndvi import MeanNdviConfigs
from .marker_config.mowing import MowingConfigs
from .marker_config.ploughing import PloughingConfigs
from .marker_config.similarity import SimilarityConfigs


class MarkerConfigs(SDKRequestBaseModel):
    """A model for the marker configurations."""

    mowing: MowingConfigs = Field(default_factory=MowingConfigs, title="Type: Mowing")
    baresoil: BaresoilConfigs = Field(default_factory=BaresoilConfigs, title="Type: Baresoil")
    distance: DistanceConfigs = Field(default_factory=DistanceConfigs, title="Type: Distance")
    similarity: SimilarityConfigs = Field(default_factory=SimilarityConfigs, title="Type: Similarity")
    mean_ndvi: MeanNdviConfigs = Field(default_factory=MeanNdviConfigs, title="Type: Mean-NDVI")
    ploughing: PloughingConfigs = Field(default_factory=PloughingConfigs, title="Type: Ploughing")
    homogeneity: HomogeneityConfigs = Field(default_factory=HomogeneityConfigs, title="Type: Homogeneity")
    greening_harvest: GreeningHarvestConfigs = Field(
        default_factory=GreeningHarvestConfigs, title="Type: Greening/Harvest"
    )
    classification: ClassificationConfigs = Field(default_factory=ClassificationConfigs, title="Type: Classification")

    @property
    def subscriptions(self) -> set[str]:
        """Return a set of all subscriptions from all marker kinds and sources."""

        return (
            self.mowing.subscriptions
            | self.baresoil.subscriptions
            | self.distance.subscriptions
            | self.similarity.subscriptions
            | self.mean_ndvi.subscriptions
            | self.ploughing.subscriptions
            | self.homogeneity.subscriptions
            | self.greening_harvest.subscriptions
            | self.classification.subscriptions
        )

    @classmethod
    def combine(cls, left: Any, right: Any) -> Self:
        """Combine two marker configurations, by taking the all right ones and only adding ones
        from left that are not present in right and doing this for all marker kinds and sources.
        Presence/Equality in this context is determined by the identifier_suffix attribute.
        """

        if not isinstance(left, cls):
            raise ValueError(f"Cannot use combine of 'MarkerConfigs' with '{type(left)}'.")

        if not isinstance(right, cls):
            raise ValueError(f"Cannot use combine of 'MarkerConfigs' with '{type(right)}'.")

        return cls(
            mowing=MowingConfigs.combine(left.mowing, right.mowing),
            baresoil=BaresoilConfigs.combine(left.baresoil, right.baresoil),
            distance=DistanceConfigs.combine(left.distance, right.distance),
            similarity=SimilarityConfigs.combine(left.similarity, right.similarity),
            mean_ndvi=MeanNdviConfigs.combine(left.mean_ndvi, right.mean_ndvi),
            ploughing=PloughingConfigs.combine(left.ploughing, right.ploughing),
            homogeneity=HomogeneityConfigs.combine(left.homogeneity, right.homogeneity),
            greening_harvest=GreeningHarvestConfigs.combine(left.greening_harvest, right.greening_harvest),
            classification=ClassificationConfigs.combine(left.classification, right.classification),
        )


class MarkersRunConfig(SDKRequestBaseModel):
    """Marker run configuration.
    Each run is associated with a unique name.
    Its input data can be subset by a list of FOI ids and the computation can be subset by a list of root nodes.
    The marker configurations define the configuration for marker types.
    User specifies one configuration per subscription.
    """

    run_name: str = Field(
        default="official",
        description="Unique ID for the specific marker computation run. "
        "If the `Signal Download Configuration` changes, e.g. user downloads additional signals by prolonging the TOI "
        "for a signal package, the run name can be reused. "
        "In case of markers recomputation using tweaked parameters or additional markers, a new run name must be "
        "chosen. Otherwise the flow will fail.",
        title="Run Name",
    )
    root_nodes_to_run: list[str] | None = Field(
        description=(
            "List of root node names in the marker computation graph. The execution finds all the ancestor nodes of "
            "the specified root nodes in marker run computation graph. Only this subgraph is executed. If a specified "
            "node does not exist, an error is raised."
        ),
        title="Root Nodes to Run",
    )
    marker_configs: MarkerConfigs = Field(
        default_factory=MarkerConfigs,
        description="Composition of all the marker configurations utilized in the run.",
        title="Marker Configurations",
    )

    @property
    def subscriptions(self) -> set[str]:
        """Return a set of all subscriptions from all marker kinds and sources."""
        return self.marker_configs.subscriptions
