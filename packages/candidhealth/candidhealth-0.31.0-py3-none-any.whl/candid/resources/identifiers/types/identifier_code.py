# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class IdentifierCode(str, enum.Enum):
    MCR = "MCR"
    MCD = "MCD"

    def visit(self, mcr: typing.Callable[[], T_Result], mcd: typing.Callable[[], T_Result]) -> T_Result:
        if self is IdentifierCode.MCR:
            return mcr()
        if self is IdentifierCode.MCD:
            return mcd()
