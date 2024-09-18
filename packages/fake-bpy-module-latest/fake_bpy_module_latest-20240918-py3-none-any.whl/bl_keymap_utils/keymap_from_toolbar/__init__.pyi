import typing
import collections.abc
import typing_extensions

_GenericType1 = typing.TypeVar("_GenericType1")
_GenericType2 = typing.TypeVar("_GenericType2")

def generate(context, space_type, *, use_fallback_keys=True, use_reset=True):
    """Keymap for popup toolbar, currently generated each time."""
