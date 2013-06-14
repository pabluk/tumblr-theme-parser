from pyparsing import alphas, Optional, Word
from pyparsing import SkipTo, makeHTMLTags


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
        self._parse_template()

        return self.rendered

    def _extract_meta_options(self):
        """Fill options dictionary with metatags of template."""
        meta_start, meta_end = makeHTMLTags("meta")
        for token, start, end in meta_start.scanString(self.template):
            if ":" in token.name:
                self.options[token.name] = token.content

    def _parse_template(self):
        """Parse a template string."""
        variable_name = Word(alphas + " ")
        variable_prefix = Optional(Word(alphas) + ":")
        variable = "{" + variable_prefix + variable_name + "}"
        variable.setParseAction(self._replace_variable)

        block_name = Word(alphas)
        block_start = "{block:" + block_name + "}"
        block_end = "{/block:" + block_name + "}"
        block = block_start + SkipTo(block_end) + block_end
        block.setParseAction(self._replace_block)

        self.rendered = (block | variable).transformString(self.template)

    def _replace_variable(self, s, l, t):
        """Replace variables."""
        var = "".join(t[1:-1])
        if var in self.options:
            return self.options[var]

    def _replace_block(self, s, l, t):
        block_name = t[1]
        block_content = t[3]
        if block_name in self.options:
            return (block_content * len(self.options[block_name]))
