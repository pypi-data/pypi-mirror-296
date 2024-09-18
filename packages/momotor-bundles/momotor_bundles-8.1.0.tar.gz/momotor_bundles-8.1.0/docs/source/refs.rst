.. _refs:

====
Refs
====

In the bundle XML file the `ref` attribute can be used to refer to another element in the same bundle.
`ref` is supported by the ``<file>``, ``<checklet>`` and ``<option>`` nodes.

The element is referred to by its `id` attribute, and must be defined at a higher level in the XML file.
When using the `ref` attribute, the node should not have any other attributes or child elements.

When accessing the elements using the API provided by this package, the `ref` attribute is automatically resolved
to the referred element.

.. note::

  `ref` is not yet implemented for creating new bundles, only when reading existing bundles.
  This is tracked in issue `#2 <https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/issues/2>`_.

API
===

.. automodule:: momotor.bundles.elements.refs
   :members:
   :undoc-members:
