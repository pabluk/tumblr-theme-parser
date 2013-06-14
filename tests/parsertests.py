#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import unittest
import tumblr_theme


class TestParserVariables(unittest.TestCase):

    def setUp(self):
        self.parser = tumblr_theme.Parser()        

    def test_parse_theme_with_simple_variable(self):
        options = {u'Title': u'My Title'}
        template = u"<title>{Title}</title>"
        expected = u'<title>My Title</title>'

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_parse_theme_with_many_variables(self):
        options = {u'Title': u'My Title', u'MetaDescription': u'A description'}
        template = u'<title>{Title}</title>\n' \
                   u'<meta name="description" content="{MetaDescription}" />'
        expected = u'<title>My Title</title>\n' \
                   u'<meta name="description" content="A description" />'

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_parse_theme_with_unknown_variable(self):
        options = {u'Title': u'My Title'}
        template = u"<article>{Unknown}</article>"
        expected = u"<article>{Unknown}</article>"

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_parse_theme_with_customized_variable(self):
        options = {u'color:Text': u'#CECECE'}
        template = u"""<style type="text/css">
                        #content {
                            color: {color:Text};
                        }
                    </style>"""
        expected = u"""<style type="text/css">
                        #content {
                            color: #CECECE;
                        }
                    </style>"""

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_parse_theme_with_customized_variable_and_spaces(self):
        options = {u'color:Content Background': u'#eee'}
        template = u"""<style type="text/css">
                        #content {
                            background-color: {color:Content Background};
                        }
                    </style>"""
        expected = u"""<style type="text/css">
                        #content {
                            background-color: #eee;
                        }
                    </style>"""

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)


class TestMetaData(unittest.TestCase):

    template_file = os.path.join(os.path.dirname(__file__), 'templates', 'example-metadata.html')

    def setUp(self):
        self.parser = tumblr_theme.Parser()
        self.options = {}
        self.template = ''
        with open(self.template_file) as f:
            self.template = f.read()

    def test_metadata_extraction(self):
        rendered = self.parser.parse_theme(self.options, self.template)

        self.assertIn('font:Title', self.options)
        self.assertEqual(self.options['font:Title'], 'Helvetica Neue')

        self.assertIn('color:Content Background', self.options)
        self.assertIn(self.options['color:Content Background'], '#fff')


if __name__ == '__main__':
    unittest.main()
