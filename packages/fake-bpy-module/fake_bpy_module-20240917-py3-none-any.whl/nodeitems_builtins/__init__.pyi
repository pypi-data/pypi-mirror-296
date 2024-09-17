import typing
import collections.abc
import typing_extensions
import nodeitems_utils

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

class SortedNodeCategory(nodeitems_utils.NodeCategory): ...

class CompositorNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

class ShaderNodeCategory(SortedNodeCategory):
    @classmethod
    def poll(cls, context):
        """

        :param context:
        """

def group_input_output_item_poll(context): ...
def group_tools_draw(_self, layout, _context): ...
def node_group_items(context): ...
def register(): ...
def unregister(): ...
