# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

import pydantic

from ....core.datetime_utils import serialize_datetime
from ....core.pydantic_utilities import deep_union_pydantic_dicts
from ...commons.types.appointment_id import AppointmentId
from ...commons.types.claim_id import ClaimId
from ...commons.types.encounter_external_id import EncounterExternalId
from ...commons.types.provider_id import ProviderId
from ...commons.types.service_line_id import ServiceLineId


class AllocationTargetCreate_ServiceLineById(pydantic.BaseModel):
    value: ServiceLineId
    type: typing.Literal["service_line_by_id"] = "service_line_by_id"

    class Config:
        frozen = True
        smart_union = True


class AllocationTargetCreate_ClaimById(pydantic.BaseModel):
    value: ClaimId
    type: typing.Literal["claim_by_id"] = "claim_by_id"

    class Config:
        frozen = True
        smart_union = True


class AllocationTargetCreate_ClaimByEncounterExternalId(pydantic.BaseModel):
    value: EncounterExternalId
    type: typing.Literal["claim_by_encounter_external_id"] = "claim_by_encounter_external_id"

    class Config:
        frozen = True
        smart_union = True


class AllocationTargetCreate_BillingProviderById(pydantic.BaseModel):
    value: ProviderId
    type: typing.Literal["billing_provider_by_id"] = "billing_provider_by_id"

    class Config:
        frozen = True
        smart_union = True


class AllocationTargetCreate_AppointmentById(pydantic.BaseModel):
    value: AppointmentId
    type: typing.Literal["appointment_by_id"] = "appointment_by_id"

    class Config:
        frozen = True
        smart_union = True


class AllocationTargetCreate_Unattributed(pydantic.BaseModel):
    """
    Allocation targets describe whether the portion of a payment is being applied toward a specific service line,
    claim, billing provider, or is unallocated.
    """

    type: typing.Literal["unattributed"] = "unattributed"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic.Extra.forbid
        json_encoders = {dt.datetime: serialize_datetime}


AllocationTargetCreate = typing.Union[
    AllocationTargetCreate_ServiceLineById,
    AllocationTargetCreate_ClaimById,
    AllocationTargetCreate_ClaimByEncounterExternalId,
    AllocationTargetCreate_BillingProviderById,
    AllocationTargetCreate_AppointmentById,
    AllocationTargetCreate_Unattributed,
]
