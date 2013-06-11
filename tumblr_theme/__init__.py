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

        self._parse_variables()

        return self.rendered

    def _parse_variables(self):
        """Parse only variables."""
        for key, value in self.options.items():
            self.rendered = self.rendered.replace("{%s}" % key, value)
