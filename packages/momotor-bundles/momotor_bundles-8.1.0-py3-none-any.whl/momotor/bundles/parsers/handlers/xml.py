from __future__ import annotations

import typing

from xsdata.exceptions import XmlHandlerError
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler


class XmlBundleEventHandler(XmlEventHandler):
    def parse(self, source: typing.Any, ns_map: dict[str | None, str]) -> typing.Any:
        """Parse the source XML document.

        Args:
            source: The xml source, can be a file resource or an input stream,
                or a xml tree/element.
            ns_map: A namespace prefix-URI recorder map

        Returns:
            An instance of the class type representing the parsed content.
        """
        if getattr(self.parser.config, 'process_xslt', None):
            raise XmlHandlerError(
                f"{type(self).__name__} doesn't support xslt transformation."
            )

        if getattr(self.parser.config, 'validation_schema_path', None):
            raise XmlHandlerError(
                f"{type(self).__name__} doesn't support validation."
            )

        return super().parse(source, ns_map)
