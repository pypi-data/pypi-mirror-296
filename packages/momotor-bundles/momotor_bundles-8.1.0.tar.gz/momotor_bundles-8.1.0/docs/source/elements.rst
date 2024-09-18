========
Elements
========

The classes in this module are used to define the structure of a bundle. All these classes are immutable.

Creating a new instance of these classes is done using the :py:meth:`~momotor.bundles.elements.base.Element.create`
method instead of the constructor, in the following way:

.. code-block:: python

   target_bundle = ...
   checklet = Checklet(bundle).create(name='checklet', ...)
   step = Step(bundle).create(id='step1', checklet=checklet, ...)

The :py:meth:`~momotor.bundles.elements.base.Element.recreate` and
:py:meth:`~momotor.bundles.elements.base.Element.recreate_list` methods can be used to create a new instance of the
class with the same attributes as the original instance, but with some of them replaced by new values.

Element base
------------

.. autoclass:: momotor.bundles.elements.base.Element
   :members:
   :inherited-members:
   :undoc-members:

Checklet
--------

.. autoclass:: momotor.bundles.elements.checklets.Checklet
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.checklets.Link
   :members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.checklets.PackageVersion
   :members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.checklets.Repository
   :members:
   :undoc-members:

File
----

.. autoclass:: momotor.bundles.elements.files.File
   :members:
   :inherited-members:
   :undoc-members:

Meta
----

.. autoclass:: momotor.bundles.elements.meta.Meta
   :members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.meta.Description
   :members:
   :inherited-members:
   :undoc-members:

Option
------

.. autoclass:: momotor.bundles.elements.options.Option
   :members:
   :inherited-members:
   :undoc-members:

Property
--------

.. autoclass:: momotor.bundles.elements.properties.Property
   :members:
   :inherited-members:
   :undoc-members:

Resource
--------

.. autoclass:: momotor.bundles.elements.resources.Resource
   :members:
   :inherited-members:
   :undoc-members:

Result
------

.. autoclass:: momotor.bundles.elements.result.Result
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.results.Results
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.result.Outcome
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.results.ResultKeyedTuple
   :members:

Step
----

.. autoclass:: momotor.bundles.elements.steps.Step
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.steps.Depends
   :members:
   :inherited-members:
   :undoc-members:

.. autoclass:: momotor.bundles.elements.steps.Priority
   :members:
   :inherited-members:
   :undoc-members:
