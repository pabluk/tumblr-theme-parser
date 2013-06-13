from pyparsing import Word, Optional, Literal, alphas, makeHTMLTags


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
        variable = "{" + Optional(Word(alphas) + ":") + Word(alphas + " ") + "}"
        variable.setResultsName('variable')
        variable.setParseAction(self._replace_variable)

        self.rendered = variable.transformString(self.template)

    def _replace_variable(self, s, l, t):
        """Replace variables."""
        var = "".join(t[1:-1])
        if var in self.options:
            return self.options[var]
