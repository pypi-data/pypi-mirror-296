
class ValidationError(ValueError):
    """ Raised when an XML validation error occurs

    This internal exception in converted to a :py:class:`~momotor.bundles.exception.BundleFormatError`
    before being thrown to the caller
    """
    pass
