# pylint: disable=too-few-public-methods

"""Base model definitions for SDK and service."""

import abc

from pydantic import BaseModel, Extra


class SDKResponseBaseModel(BaseModel):
    """Base model for SDK response objects. Ignores extra fields."""

    class Config:
        extra = Extra.ignore
        validate_assignment = True
        frozen = True
        validate_all = True


class SDKRequestBaseModel(BaseModel):
    """Base model for SDK request objects. Forbids extra fields."""

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        frozen = True
        validate_all = True


class SDKRequestCredentials(BaseModel):
    """Base model for credentials used in client to client communication."""

    @abc.abstractmethod
    def to_request_dict(self) -> dict[str, str]:
        """Transforms the credentials into a dictionary that can be used in a request."""

    class Config:
        """Extra.ignore is used so "type" ("S3", "SENTINEL_HUB", ...) can be added to the request."""

        extra = Extra.ignore
        validate_assignment = True
        frozen = True
        validate_all = True
