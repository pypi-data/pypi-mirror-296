"""
This module provides access to bmesh geometry evaluation functions.

"""

import typing
import collections.abc
import typing_extensions
import bmesh.types
import mathutils

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

def intersect_face_point(
    face: bmesh.types.BMFace, point: collections.abc.Sequence[float] | mathutils.Vector
) -> bool:
    """Tests if the projection of a point is inside a face (using the face's normal).

    :param face: The face to test.
    :type face: bmesh.types.BMFace
    :param point: The point to test.
    :type point: collections.abc.Sequence[float] | mathutils.Vector
    :return: True when the projection of the point is in the face.
    :rtype: bool
    """
