# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class EncounterSubmissionOriginType(str, enum.Enum):
    CANDID = "CANDID"
    EXTERNAL = "EXTERNAL"

    def visit(self, candid: typing.Callable[[], T_Result], external: typing.Callable[[], T_Result]) -> T_Result:
        if self is EncounterSubmissionOriginType.CANDID:
            return candid()
        if self is EncounterSubmissionOriginType.EXTERNAL:
            return external()
