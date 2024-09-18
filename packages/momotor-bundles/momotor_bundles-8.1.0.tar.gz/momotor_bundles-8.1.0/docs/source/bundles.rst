=======
Bundles
=======

There is a class for each bundle type:
:py:class:`~momotor.bundles.ConfigBundle`,
:py:class:`~momotor.bundles.ProductBundle`,
:py:class:`~momotor.bundles.RecipeBundle`,
:py:class:`~momotor.bundles.ResultsBundle`, and
:py:class:`~momotor.bundles.TestResultBundle`.

All classes implement the same basic functionality to implement reading and writing bundles,
plus functionality specific to the bundle type.

Bundle base
-----------

:py:class:`~momotor.bundles.Bundle` is the base class from which all other bundle types extend. It provides the shared
functionality for all bundle classes.

The constructor creates a new uninitialized bundle. The
:py:meth:`~momotor.bundles.Bundle.create` method is used to initialize a newly created bundle, the class methods
:py:meth:`~momotor.bundles.Bundle.from_bytes_factory` and :py:meth:`~momotor.bundles.Bundle.from_file_factory`
are used load a bundle from either a :py:obj:`bytes` (or more specifically a :py:obj:`memoryview`) object or a file.

The methods :py:meth:`~momotor.bundles.Bundle.to_buffer`, :py:meth:`~momotor.bundles.Bundle.to_directory`, and
:py:meth:`~momotor.bundles.Bundle.to_file` are used to export a bundle to various formats. A bundle must be
fully initialized before it can be exported.

Bundles are immutable, it's not possible to modify a bundle once it has been created. The bundle and
each element have :py:meth:`~momotor.bundles.elements.base.Element.recreate`
and :py:meth:`~momotor.bundles.elements.base.Element.recreate_list` methods to
copy elements from one bundle to another optionally with modifications to (some of the) attributes.

.. autoclass:: momotor.bundles.Bundle
   :members:
   :exclude-members: recreate
   :inherited-members:

ConfigBundle
------------

A :py:class:`~momotor.bundles.ConfigBundle` contains all configuration needed by the recipe.
It provides a Python interface to read and create XML files of
:py:class:`~momotor.bundles.binding.momotor_1_0.ConfigComplexType`

See the documentation of the base class :py:class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ConfigBundle
   :members: create,
             id, meta,
             options, get_options, get_option_value,
             files, copy_files_to

ProductBundle
-------------

A :py:class:`~momotor.bundles.ProductBundle` contains the product to be evaluated by the recipe.
It provides a Python interface to read and create XML files of
:py:class:`~momotor.bundles.binding.momotor_1_0.ProductComplexType`

See the documentation of the base class :py:class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ProductBundle
   :members: create,
             id, meta,
             options, get_options, get_option_value,
             files, copy_files_to,
             properties, get_properties, get_property_value

RecipeBundle
------------

A :py:class:`~momotor.bundles.RecipeBundle` describes the process of processing a product into a result.
It provides a Python interface to read and create XML files of
:py:class:`~momotor.bundles.binding.momotor_1_0.RecipeComplexType`

See the documentation of the base class :py:class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.RecipeBundle
   :members: create,
             id, meta,
             steps, tests,
             options, get_options, get_option_value,
             files, copy_files_to

ResultsBundle
-------------

A :py:class:`~momotor.bundles.ResultsBundle` contains the results of the recipe applied to a product.
It provides a Python interface to read and create XML files of
:py:class:`~momotor.bundles.binding.momotor_1_0.ResultsComplexType`

It also implements all methods and properties inherited :py:class:`~momotor.bundles.elements.results.Results`

See the documentation of the base class :py:class:`~momotor.bundles.Bundle` on how to use bundles.

.. autoclass:: momotor.bundles.ResultsBundle
   :members: create,
             id, meta,
             results

.. autofunction:: momotor.bundles.results.create_error_result_bundle

TestResultBundle
----------------

A :py:class:`~momotor.bundles.TestResultBundle` contains the results of a recipe's self-test.
It provides a Python interface to read and create XML files of
:py:class:`~momotor.bundles.binding.momotor_1_0.TestResultComplexType`

See the documentation of the base class :py:class:`~momotor.bundles.Bundle` on how to use bundles.

.. note::

   Self-testing bundles are not yet implemented in Momotor, this interface is subject
   to change when testing gets implemented.

.. autoclass:: momotor.bundles.TestResultBundle
   :members: create, results
