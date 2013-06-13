from pyparsing import Word, Literal, alphas


class Parser(object):
    """A Tumblr theme parser."""

    def __init__(self):
        self.template = ""
        self.rendered = ""
        self.options = {}

    def parse_theme(self, options, template):
        """Parse a template string with JSON options."""
        self.options = options
        self.template = template
        self.rendered = template

        lbracket = Literal("{")
        rbracket = Literal("}")
        variable = lbracket + Word(alphas) + rbracket
        variable.setParseAction(self._replace_variable)

        return variable.transformString(template)

    def _replace_variable(self, s, l, t):
        """Replace variables."""
        var = t[1]
        if var in self.options:
            return self.options[var]
