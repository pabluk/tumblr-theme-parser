from pyparsing import alphas, Optional, Word
from pyparsing import SkipTo, makeHTMLTags, oneOf


class Parser(object):
    """A Tumblr theme parser."""

    def __init__(self):
        self.template = ""
        self.rendered = ""
        self.options = {}

    def parse_theme(self, options, template):
        """Parse a template string with a dict of options."""
        self.options = options
        self.template = template
        self.rendered = template

        self._extract_meta_options()
        self.rendered = self._parse_template(self.options, self.template)

        return self.rendered

    def _extract_meta_options(self):
        """Fill options dictionary with metatags of template."""
        meta_start, meta_end = makeHTMLTags("meta")
        for token, start, end in meta_start.scanString(self.template):
            if ":" in token.name:
                value = token.content
                if token.name.startswith('if:'):
                    value = bool(int(value))
                self.options[token.name] = value

    def _parse_template(self, options, template):
        """Parse a template string."""
        variable_name = Word(alphas + " ")
        variable_prefix = Optional(Word(alphas) + ":")
        variable = "{" + variable_prefix + variable_name + "}"
        variable.setParseAction(self._replace_variable(options))

        block_name = oneOf("Title Description PreviousPage NextPage")
        block_start = "{block:" + block_name + "}"
        block_end = "{/block:" + block_name + "}"
        block = block_start + SkipTo(block_end) + block_end
        block.setParseAction(self._replace_block(options))

        block_type_name = oneOf("Text Photo Panorama Photoset Quote Link Chat Video Audio")
        block_type_start = "{block:" + block_type_name + "}"
        block_type_end = "{/block:" + block_type_name + "}"
        block_type = block_type_start + SkipTo(block_type_end) + block_type_end
        block_type.setParseAction(self._replace_block_type(options))

        block_iter_name = oneOf("Posts")
        block_iter_start = "{block:" + block_iter_name + "}"
        block_iter_end = "{/block:" + block_iter_name + "}"
        block_iter = block_iter_start + SkipTo(block_iter_end) + block_iter_end
        block_iter.setParseAction(self._replace_block_iter(options))

        parser = (block | block_type | block_iter | variable)
        return parser.transformString(template)

    def _replace_variable(self, options):
        """Replace variables."""
        def conversionParseAction(s, l, t):
            var = "".join(t[1:-1])
            if var in options:
                return options[var]
        return conversionParseAction

    def _replace_block(self, options):
        """Replace blocks."""
        def conversionParseAction(s, l, t):
            block_name = t[1]
            block_content = t[3]
            if block_name in options:
                return self._parse_template(options, block_content)
            else:
                return ""
        return conversionParseAction

    def _replace_block_type(self, options):
        """Replace by type of post."""
        def conversionParseAction(s, l, t):
            block_name = t[1]
            block_content = t[3]
            if block_name.lower() == options['PostType']:
                return self._parse_template(options, block_content)
            else:
                return ""
        return conversionParseAction

    def _replace_block_iter(self, options):
        """Replace blocks with content from an iterable."""
        def conversionParseAction(s, l, t):
            block_name = t[1]
            block_content = t[3]
            if block_name in options:
                rendered = ""
                for element in options[block_name]:
                    rendered += self._parse_template(element, block_content)
                return rendered
        return conversionParseAction
