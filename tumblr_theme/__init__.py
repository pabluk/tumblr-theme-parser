from pyparsing import Word, Optional, Literal, alphas


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

        variable = "{" + Optional(Word(alphas) + ":") + Word(alphas + " ") + "}"
        variable.setResultsName('variable')
        variable.setParseAction(self._replace_variable)

        return variable.transformString(template)

    def _replace_variable(self, s, l, t):
        """Replace variables."""
        var = "".join(t[1:-1])
        if var in self.options:
            return self.options[var]
