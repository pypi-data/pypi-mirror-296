from __future__ import annotations

import typing
from functools import lru_cache

try:
    from lxml import etree
    from xsdata.formats.dataclass.parsers.handlers.lxml import LxmlEventHandler, EVENTS

except ImportError:
    LxmlBundleEventHandler = None

else:
    from .exceptions import ValidationError


    @lru_cache(maxsize=16)
    def _get_schema(path: str) -> etree.XMLSchema:
        with open(path) as schema_file:
            return etree.XMLSchema(file=schema_file)

    class LxmlBundleEventHandler(LxmlEventHandler):
        """ Extends :py:class:`~xsdata.formats.dataclass.parsers.handlers.LxmlEventHandler`
        to add support for large documents and XSLT
        """
        def parse(self, source: typing.Any, ns_map: dict[str | None, str]) -> typing.Any:
            """Parse the source XML document.

            Args:
                source: The xml source, can be a file resource or an input stream,
                    or a lxml tree/element.
                ns_map: A namespace prefix-URI recorder map

            Returns:
                An instance of the class type representing the parsed content.
            """
            lxml_parser = etree.XMLParser(
                huge_tree=getattr(self.parser.config, 'huge_tree', True),
                recover=True,
                remove_comments=True,
            )

            tree = etree.parse(
                source,
                parser=lxml_parser,
                base_url=self.parser.config.base_url
            )

            if getattr(self.parser.config, 'process_xslt', True):
                stylesheet = tree.xpath('//processing-instruction("xml-stylesheet")')
                if stylesheet:
                    xsl = stylesheet[0].parseXSL()
                    xsl.xinclude()
                    tree = tree.xslt(xsl)

            if self.parser.config.process_xinclude:
                tree.xinclude()

            validation_schema_path = getattr(self.parser.config, 'validation_schema_path', True)
            if validation_schema_path:
                schema = _get_schema(str(validation_schema_path))
                try:
                    schema.assertValid(tree)
                except etree.DocumentInvalid as e:
                    raise ValidationError(str(e))

            ctx = etree.iterwalk(tree, EVENTS)

            return self.process_context(ctx, ns_map)
