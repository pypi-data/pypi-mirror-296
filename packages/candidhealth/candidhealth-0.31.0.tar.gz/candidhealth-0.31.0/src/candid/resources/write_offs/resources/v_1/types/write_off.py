# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....commons.types.claim_id import ClaimId
from .....commons.types.patient_external_id import PatientExternalId
from .....commons.types.service_line_id import ServiceLineId
from .....payers.resources.v_3.types.payer import Payer
from .insurance_write_off_reason import InsuranceWriteOffReason
from .insurance_write_off_target import InsuranceWriteOffTarget
from .patient_write_off_reason import PatientWriteOffReason
from .write_off_id import WriteOffId


class WriteOff_Patient(pydantic.BaseModel):
    write_off_id: WriteOffId
    write_off_timestamp: dt.datetime
    write_off_note: typing.Optional[str] = None
    write_off_reason: PatientWriteOffReason
    patient_external_id: PatientExternalId
    claim_id: ClaimId
    service_line_id: ServiceLineId
    reverts_write_off_id: typing.Optional[WriteOffId] = None
    reverted_by_write_off_id: typing.Optional[WriteOffId] = None
    amount_cents: int
    type: typing.Literal["patient"] = "patient"

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


class WriteOff_Insurance(pydantic.BaseModel):
    write_off_id: WriteOffId
    payer: Payer
    write_off_target: InsuranceWriteOffTarget
    write_off_timestamp: dt.datetime
    write_off_note: typing.Optional[str] = None
    write_off_reason: InsuranceWriteOffReason
    reverts_write_off_id: typing.Optional[WriteOffId] = None
    reverted_by_write_off_id: typing.Optional[WriteOffId] = None
    amount_cents: int
    type: typing.Literal["insurance"] = "insurance"

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


WriteOff = typing.Union[WriteOff_Patient, WriteOff_Insurance]
