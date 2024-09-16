import typing
import collections.abc
import typing_extensions

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

class RestrictBlend:
    context: typing.Any
    data: typing.Any

class _RestrictContext:
    preferences: typing.Any
    window_manager: typing.Any

class _RestrictData: ...
