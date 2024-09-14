# pylint: disable=too-few-public-methods

"""Module for the Classification standard marker configurations."""

from datetime import date

from pydantic import Field, PositiveFloat, PositiveInt, validator

from .base import BaseMarkerConfigs, BaseStandardMarkerConfig
from .utils import validate_start_and_end_date_consistency


class BaseClassification(BaseStandardMarkerConfig):
    """Base class for classification configurations.

    Classification marker is supported on AP (agricultural parcels) and LU (land use parcels).
    Multiple subscriptions for training are also supported.

    The Classification marker can be separately customized for the two supported sources (S2L2A and PF).
    The flow produces one prediction per source, there is no interaction between the two.
    """

    classification_start_date: date = Field(
        title="Classification Start Date",
        description="Defines a start date for observations used in Classification marker in format 'YYYY-MM-DD'.",
    )
    classification_end_date: date = Field(
        title="Classification End Date",
        description="Defines an end date for observations used in Classification marker in format 'YYYY-MM-DD'.",
    )

    class_label_mapping_path: str = Field(title="Path to class-label mapping JSON.")
    class_group_mapping_path: str | None = Field(None, title="Path to class-group to class-label mapping JSON.")

    legacy_signals_path: str | None = Field(None, title="Path to legacy signals dataset to be used in training.")

    additional_subscription_codes: list[str] = Field(
        default_factory=list,
        title="Additional Subscription Codes.",
        description="Additional subscription codes for signals to train on. "
        "This enables training on non-primary subscriptions.",
    )

    well_represented_thr: int = Field(
        0,
        title="Well-represented threshold",
        description="Minimum nuuumber of current year FOIs in one label class to avoid using legacy signals.",
    )

    n_folds: PositiveInt = Field(
        4,
        title="Number of folds generated from input datasets",
        description=(
            "Leave One Out Cross Validation (LOOCV) is being performed to avoid overfitting."
            "Each fold contains all but `1 / n_folds` observations. This results in `n_folds different models. "
            "Each model prediction is then taken into account to produce robust and generizable results. "
            "Low `n_folds` leads to overfit results, while higher `n_folds` leads to higher variation in models, "
            "use with caution."
        ),
    )

    hash_id_col: str = Field(
        "POLY_ID",
        title="Hash ID Column",
        description="Column name used for fold assignment and prediction sampling. It is used to ensure "
        "that certain FOIs do not get overrepresented in the training set. The column must exist "
        "in the input reference dataset and be of the type that can be cast to string.  "
        "Complex types like dictionaries are not allowed.  ",
    )
    lstm_layers: PositiveInt = Field(
        3,
        title="Number of RNN layers in the neural network",
        description="Number of recurrent layers. "
        "Setting `num_layers=2` would mean stacking two LSTMs together to form a stacked LSTM, "
        "with the second LSTM taking in outputs of the first LSTM and computing the final results.",
    )
    lstm_dims: PositiveInt = Field(
        128,
        title="LSTM Hidden Dimension",
        description="LSTM models maintain the hidden state, which act as a short-term mermory of the network. "
        "By adjusting the number of hidden layers, we regulate the short-term memory capacity of the model. "
        "The usage of default values is suggested.",
    )
    lstm_dropout: PositiveFloat = Field(
        0.2,
        title="If non-zero, introduces a Dropout layer on the outputs of each LSTM layer except the last layer, "
        "with dropout probability equal to specified parameter.",
    )

    # Early stopping parameters.
    min_delta: PositiveFloat = Field(
        0.05,
        description="The amount of validation loss increase after which we consider model to not improve. "
        "Simply put, if an epoch's validation loss is bigger than previous one's for more than `min_delta`, "
        "the procedure starts counting epochs until we reach `patience` number of epoch or reach "
        "a new 'best' epoch candidate.",
    )
    patience: PositiveInt = Field(
        5,
        title="Patience",
        description="When in training, model performance is being monitored through observing validation loss. "
        "Patience defines the maximum number of epochs in which no improvement is noticed. If it is exceeded, "
        "training is stopped.",
    )

    @validator("classification_start_date", pre=True, allow_reuse=True)
    @classmethod
    def parse_start_date(cls, v: object) -> object:
        """Parse the start date from a string to a date object."""

        return date.fromisoformat(v) if isinstance(v, str) else v

    @validator("classification_end_date", pre=True, allow_reuse=True)
    @classmethod
    def parse_end_date(cls, v: object) -> object:
        """Parse the end date from a string to a date object."""

        return date.fromisoformat(v) if isinstance(v, str) else v

    @validator("classification_end_date", allow_reuse=True)
    @classmethod
    def validate_end_date(cls, v: date, values: dict[str, str | date]) -> str | date:
        """Validate the end date is after the start date."""

        start_date = values["classification_start_date"]
        validate_start_and_end_date_consistency(start_date=start_date, end_date=v)
        return v


class S2L2AClassification(BaseClassification):
    """Configuration for the S2L2A classification marker."""

    valid_query: str = Field("CLP <= 0.4 and OUT_PROBA <= 0.8", title="Valid Query")
    train_cols: list[str] = Field(
        [
            "B01",
            "B02",
            "B03",
            "B04",
            "B05",
            "B06",
            "B07",
            "B08",
            "B8A",
            "B09",
            "B11",
            "B12",
            "CLP",
        ],
        title="Ids of columns used in LSTM training.",
        min_items=1,
        unique_items=True,
    )
    n_timestamps: int = Field(70, title="Number of timestamps for a single FOI to be used in LSTM training.")
    batch_size: int = Field(4096, title="Size of a single training batch.")


class PFClassification(BaseClassification):
    """Configuration for the PF classification marker."""

    valid_query: str = Field("abs(DAYS_TO_NEAREST_OBS)<=1", title="Valid Query")
    train_cols: list[str] = Field(
        ["SR1", "SR2", "SR3", "SR4", "NDVI", "CL_RED", "CL_GREEN"],
        title="Ids of columns used in LSTM training.",
        min_items=1,
        unique_items=True,
    )
    n_timestamps: int = Field(180, title="Number of timestamps for a single FOI to be used in LSTM training.")
    batch_size: int = Field(2048, title="Size of a single training batch.")


class ClassificationConfigs(BaseMarkerConfigs[S2L2AClassification, PFClassification]):
    """Configurations for the Classification standard marker.

    Classification marker is used to train a LSTM model and use it to classify the FOIs based on time series data.
    """

    S2L2A: list[S2L2AClassification] = Field(default_factory=list, title="Source: S2L2A")
    PF: list[PFClassification] = Field(default_factory=list, title="Source: PF")
