# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ......core.datetime_utils import serialize_datetime
from ......core.pydantic_utilities import deep_union_pydantic_dicts
from .....commons.types.date import Date
from .....commons.types.regions import Regions
from .authorized_signatory import AuthorizedSignatory
from .contract_status import ContractStatus
from .insurance_types import InsuranceTypes


class ContractBase(pydantic.BaseModel):
    effective_date: Date = pydantic.Field()
    """
    The starting day upon which the contract is effective
    """

    expiration_date: typing.Optional[Date] = pydantic.Field(default=None)
    """
    An optional end day upon which the contract expires
    """

    regions: Regions = pydantic.Field()
    """
    The state(s) to which the contract's coverage extends.
    It may also be set to "national" for the entirety of the US.
    """

    contract_status: typing.Optional[ContractStatus] = None
    authorized_signatory: typing.Optional[AuthorizedSignatory] = None
    commercial_insurance_types: InsuranceTypes = pydantic.Field()
    """
    The commercial plan insurance types this contract applies.
    """

    medicare_insurance_types: InsuranceTypes = pydantic.Field()
    """
    The Medicare plan insurance types this contract applies.
    """

    medicaid_insurance_types: InsuranceTypes = pydantic.Field()
    """
    The Medicaid plan insurance types this contract applies.
    """

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
