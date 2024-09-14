# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .application_configuration import ApplicationConfiguration

__all__ = [
    "ApplicationVariantRetrieveResponse",
    "ApplicationVariantV0Response",
    "ApplicationVariantAgentsServiceResponse",
    "OfflineApplicationVariantResponse",
    "OfflineApplicationVariantResponseConfiguration",
]


class ApplicationVariantV0Response(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ApplicationConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    version: Literal["V0"]

    description: Optional[str] = None
    """Optional description of the application variant"""


class ApplicationVariantAgentsServiceResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    version: Literal["AGENTS_SERVICE"]

    configuration: Optional[object] = None

    description: Optional[str] = None
    """Optional description of the application variant"""


class OfflineApplicationVariantResponseConfiguration(BaseModel):
    metadata: Optional[object] = None
    """User defined metadata about the offline application"""

    output_schema_type: Optional[Literal["completion_only", "context_string", "context_chunks"]] = None
    """An enumeration."""


class OfflineApplicationVariantResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: OfflineApplicationVariantResponseConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    version: Literal["OFFLINE"]

    description: Optional[str] = None
    """Optional description of the application variant"""


ApplicationVariantRetrieveResponse: TypeAlias = Annotated[
    Union[ApplicationVariantV0Response, ApplicationVariantAgentsServiceResponse, OfflineApplicationVariantResponse],
    PropertyInfo(discriminator="version"),
]
