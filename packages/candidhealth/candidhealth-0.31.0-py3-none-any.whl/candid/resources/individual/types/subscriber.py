# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ....core.datetime_utils import serialize_datetime
from ....core.pydantic_utilities import deep_union_pydantic_dicts
from ...insurance_cards.resources.v_2.types.insurance_card import InsuranceCard
from .individual_id import IndividualId
from .subscriber_base import SubscriberBase


class Subscriber(SubscriberBase):
    """
    Examples
    --------
    import datetime
    import uuid

    from candid import (
        Gender,
        InsuranceTypeCode,
        PatientRelationshipToInsuredCodeAll,
        SourceOfPaymentCode,
        State,
        StreetAddressShortZip,
        Subscriber,
    )
    from candid.resources.insurance_cards.v_2 import InsuranceCard

    Subscriber(
        individual_id=uuid.UUID(
            "797348a9-e7e8-4e59-8628-95390d079c0b",
        ),
        insurance_card=InsuranceCard(
            insurance_card_id=uuid.UUID(
                "ca5b7711-4419-4161-9b7c-3494ac40c8d4",
            ),
            member_id="E85313B4-0FFC-4119-8042-8161A4ECFF0A",
            payer_name="John Doe",
            payer_id="836DDAA6-863F-4020-ACCA-205A689F0002",
            rx_bin="610014",
            rx_pcn="MEDDPRIME",
            image_url_front="https://s3.amazonaws.com/front.jpg",
            image_url_back="https://s3.amazonaws.com/back.jpg",
            group_number="ABC12345",
            plan_name="Silver PPO Plan",
            plan_type=SourceOfPaymentCode.SELF_PAY,
            insurance_type=InsuranceTypeCode.C_12,
        ),
        patient_relationship_to_subscriber_code=PatientRelationshipToInsuredCodeAll.SPOUSE,
        date_of_birth=datetime.date.fromisoformat(
            "2000-01-01",
        ),
        address=StreetAddressShortZip(
            address_1="123 Main St",
            address_2="Apt 1",
            city="New York",
            state=State.NY,
            zip_code="10001",
            zip_plus_four_code="1234",
        ),
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
    )
    """

    individual_id: IndividualId
    insurance_card: InsuranceCard

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
        allow_population_by_field_name = True
        populate_by_name = True
        extra = pydantic.Extra.forbid
        json_encoders = {dt.datetime: serialize_datetime}
