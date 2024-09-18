from __future__ import annotations

import collections.abc
import typing

from momotor.bundles.binding import FileComplexType, OptionComplexType, CheckletComplexType
from momotor.bundles.exception import InvalidRefError
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['resolve_ref']


CT = typing.TypeVar('CT', bound=typing.Union[FileComplexType, OptionComplexType, CheckletComplexType])


def resolve_ref(tag_name: str, node: CT, groups: collections.abc.Iterable[collections.abc.Iterable[object]]) \
        -> tuple[object | None, CT]:
    """ Resolve reference. Used internally by the classes implementing referable nodes, so there should be
    no need to call this method directly.

    :param tag_name: tag name of referenced node
    :param node: node to resolve reference of (should have a ``ref`` attribute)
    :param groups: parent groups to search the reference in
    :return: a `tuple` (`parent`, `node`).
        `parent` can be ``None``, in that case, ref attribute was ``None`` and provided node is returned.
        Otherwise, returns the resolved reference.
    :raises: :py:exc:`~momotor.bundles.exception.InvalidRefError` when reference cannot be resolved
    """

    ref = node.ref
    if not ref:
        return None, node

    for group in groups:
        if group:
            for parent in group:
                for name, ref_node in get_nested_complex_nodes(parent, tag_name):
                    ref_node = typing.cast(CT, ref_node)
                    if ref_node.id == node.ref:
                        return parent, ref_node

    raise InvalidRefError("Unable to find {} id={}".format(tag_name, ref))
