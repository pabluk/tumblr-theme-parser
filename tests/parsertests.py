#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import unittest
import tumblr_theme


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = tumblr_theme.Parser()        

    def test_parse_theme_with_simple_variable(self):
        options = {u'Title': u'My Title'}
        template = u"<title>{Title}</title>"
        result = u'<title>My Title</title>'

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(result, rendered)

    def test_parse_theme_with_many_variable(self):
        options = {u'Title': u'My Title', u'MetaDescription': u'A description'}
        template = u'<title>{Title}</title>\n' \
                   u'<meta name="description" content="{MetaDescription}" />'
        result = u'<title>My Title</title>\n' \
                   u'<meta name="description" content="A description" />'

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(result, rendered)

    def test_parse_theme_with_unknown_variable(self):
        options = {u'Title': u'My Title'}
        template = u"<article>{Unknown}</article>"
        result = u"<article>{Unknown}</article>"

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(result, rendered)


if __name__ == '__main__':
    unittest.main()
