import typing
import collections.abc
import typing_extensions

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

def compat_str(text, line_length=0): ...
def graph_armature(
    obj, filepath, FAKE_PARENT=True, CONSTRAINTS=True, DRIVERS=True, XTRA_INFO=True
): ...
