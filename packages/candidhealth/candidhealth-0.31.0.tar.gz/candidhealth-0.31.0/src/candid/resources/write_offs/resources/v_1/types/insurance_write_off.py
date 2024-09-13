# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....payers.resources.v_3.types.payer import Payer
from .insurance_write_off_reason import InsuranceWriteOffReason
from .insurance_write_off_target import InsuranceWriteOffTarget
from .write_off_id import WriteOffId


class InsuranceWriteOff(pydantic.BaseModel):
    write_off_id: WriteOffId
    payer: Payer
    write_off_target: InsuranceWriteOffTarget
    write_off_timestamp: dt.datetime
    write_off_note: typing.Optional[str] = None
    write_off_reason: InsuranceWriteOffReason
    reverts_write_off_id: typing.Optional[WriteOffId] = None
    reverted_by_write_off_id: typing.Optional[WriteOffId] = None
    amount_cents: int

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
