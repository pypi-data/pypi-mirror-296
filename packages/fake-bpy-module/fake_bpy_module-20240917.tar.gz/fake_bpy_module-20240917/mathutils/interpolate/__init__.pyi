"""
The Blender interpolate module

"""

import typing
import collections.abc
import typing_extensions

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

def poly_3d_calc(veclist, pt):
    """Calculate barycentric weights for a point on a polygon.

    :param veclist: list of vectors
    :param pt: point   :rtype: list of per-vector weights
    """
