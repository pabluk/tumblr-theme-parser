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
                self.options[token.name] = token.content

    def _parse_template(self, options, template):
        """Parse a template string."""
        variable_name = Word(alphas + " ")
        variable_prefix = Optional(Word(alphas) + ":")
        variable = "{" + variable_prefix + variable_name + "}"
        variable.setParseAction(self._replace_variable(options))

        block_name = oneOf("Posts")
        block_start = "{block:" + block_name + "}"
        block_end = "{/block:" + block_name + "}"
        block = block_start + SkipTo(block_end) + block_end
        block.setParseAction(self._replace_block(options))

        return (block | variable).transformString(self.template)

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
                rendered = ""
                for element in options[block_name]:
                    rendered += block_content
                return rendered
        return conversionParseAction
