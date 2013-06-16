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


class TestBlocks(unittest.TestCase):

    def setUp(self):
        self.template_dir = os.path.join(os.path.dirname(__file__),
            'templates')
        self.parser = tumblr_theme.Parser()

    def test_block_posts(self):
        options = {
            u'Posts': [
                {'Title': 'Title 1', 'Body': 'Body of the post 1.'},
                {'Title': 'Title 2', 'Body': 'Body of the post 2.'},
                {'Title': 'Title 3', 'Body': 'Body of the post 3.'},
                {'Title': 'Title 4', 'Body': 'Body of the post 4.'}
            ]
        }
        template = u"""
            <ol id="posts">
                {block:Posts}
                    <li> ... </li>
                {/block:Posts}
            </ol>"""
        expected = u"""
            <ol id="posts">
                <li> ... </li>
                <li> ... </li>
                <li> ... </li>
                <li> ... </li>
                
            </ol>"""

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_block_post_content(self):
        template_file = os.path.join(self.template_dir,
            'block-post-content.html')
        with open(template_file) as f:
            template = f.read()
        expected_file = os.path.join(self.template_dir,
            'block-post-content_expected.html')
        with open(expected_file) as f:
            expected = f.read()

        options = {
            u'Posts': [
                {
                    'Title': 'Title 1',
                    'Body': 'Body of the post 1.',
                    'PostType': 'text',
                    'Permalink': '/post/1/'
                },
                {
                    'Title': 'Title 2',
                    'Body': 'Body of the post 2.',
                    'PostType': 'text',
                    'Permalink': '/post/2/'
                },
                {
                    'Title': 'Title 3',
                    'Body': 'Body of the post 3.',
                    'PostType': 'text',
                    'Permalink': '/post/3/'
                },
            ]
        }

        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)

    def test_block_conditional(self):
        template_file = os.path.join(self.template_dir,
            'meta-if-tags.html')
        with open(template_file) as f:
            template = f.read()
        expected_file = os.path.join(self.template_dir,
            'meta-if-tags_expected.html')
        with open(expected_file) as f:
            expected = f.read()

        options = {}
        rendered = self.parser.parse_theme(options, template)
        self.assertEqual(expected, rendered)


class TestMetaData(unittest.TestCase):

    template_file = os.path.join(
        os.path.dirname(__file__),
        'templates',
        'example-metadata.html')

    def setUp(self):
        self.options = {}
        self.template = ''
        with open(self.template_file) as f:
            self.template = f.read()
        self.parser = tumblr_theme.Parser()
        self.parser.parse_theme(self.options, self.template)

    def test_metadata_extraction(self):
        self.assertIn('font:Title', self.options)
        self.assertEqual(self.options['font:Title'], 'Helvetica Neue')

    def test_metadata_extraction_with_spaces(self):
        self.assertIn('color:Content Background', self.options)
        self.assertIn(self.options['color:Content Background'], '#fff')

    def test_metadata_extraction_with_if(self):
        self.assertIn('if:Show Main Nav', self.options)
        self.assertTrue(self.options['if:Show Main Nav'])

    def test_metadata_extraction_with_if_false(self):
        self.assertIn('if:Show Tags', self.options)
        self.assertFalse(self.options['if:Show Tags'])


if __name__ == '__main__':
    unittest.main()
