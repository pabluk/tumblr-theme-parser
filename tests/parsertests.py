#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import unittest
import tumblr_theme


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = tumblr_theme.Parser()        

    def test_parse_theme_with_variables(self):
        options = {u'Title': u'My Title'}
        template = u"<title>{Title}</title>"
        rendered = self.parser.parse_theme(options, template)

        self.assertEqual(rendered, u'<title>My Title</title>')


if __name__ == '__main__':
    unittest.main()
