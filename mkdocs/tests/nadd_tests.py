#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import io
import unittest
from datetime import date, datetime
import os
import tempfile

from mkdocs.commands import add, new


class AddTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)
        new.new("myproject", None)
        os.chdir("myproject")

        # Setup config for test
        io.open('_template/test.md', 'w', encoding='utf-8').write(
            "{{filename}} created at {{datetime}}"
        )

        # Append new conf to config file
        yaml_conf = """test:
          filename:
            type: filename
          datetime:
            type: datetime
            options:
              format: '%A %B %Y at %X'
        """
        io.open('_template/_config.yml', 'a', encoding='utf-8').write(yaml_conf)

    def test_add(self):
        expect = """testadd created at {0}""".format((datetime.now()).strftime('%A %B %Y at %X'))
        add.add('test', './', 'testadd')
        self.assertEqual(io.open(os.path.join(os.getcwd(), 'docs', 'testadd.md'), 'r').read(), expect)

    # Is current working directory a mkdocs project
    def test_is_cwd_mkdocs_project(self):
        self.assertTrue(add._is_cwd_mkdocs_project())

    # Is current working directory as a template directory
    def test_is_cwd_as_template_directory(self):
        self.assertTrue(add._is_cwd_as_template_directory('_template'))
        self.assertFalse(add._is_cwd_as_template_directory('dir_error'))

    # As template in template directory
    def test_as_template_in_template_directory(self):
        self.assertTrue(add._as_template_in_template_directory('_template/sample.md'))
        self.assertFalse(add._as_template_in_template_directory('_template/testfalse.md'))

    # As config in template directory
    def test_as_config_in_template_directory(self):
        self.assertTrue(add._as_config_in_template_directory('_template'))
        self.assertFalse(add._as_config_in_template_directory('_test'))

    # As not file in docs directory
    def test_as_not_file_in_docs_directory(self):
        self.assertFalse(add._as_not_file_in_docs_directory('docs/index.md'))
        self.assertTrue(add._as_not_file_in_docs_directory('no_file_in_dir'))

    # As output directory
    def test_as_output_directory(self):
        os.mkdir('docs/output')
        self.assertTrue(add._as_output_directory('docs/output', False))
        os.rmdir('docs/output')
        self.assertFalse(add._as_output_directory('output', False))
        self.assertTrue(add._as_output_directory('docs/output', True))

    # Get config file
    def test_get_config_file(self):
        expect = {
            'filename': {'type': 'filename'},
            'datetime': {'type': 'datetime'},
            'datetime_format': {'type': 'datetime', 'options': {'format': '%A %B %Y at %X'}},
            'date': {'type': 'date'},
            'date_format': {'type': 'date', 'options': {'format': '%x'}},
            'text': {'type': 'text', 'value': 'Lorem ipsum dolor sit amet'}
        }
        self.assertEqual(add._get_config_file('_template', 'sample'), expect)
        self.assertIsNone(add._get_config_file('_template', 'undefined'))

    # Check existance
    def test_check_existance(self):
        self.assertTrue(add._check_existance('_template',
                                             '_template/sample.md',
                                             './',
                                             './sample.md',
                                             True))
        self.assertFalse(add._check_existance('_scaffold',
                                              '_scaffold/sample.md',
                                              './',
                                              './sample.md',
                                              True))

    # Write file
    def test_write_file(self):
        config = {
            'filename': {'type': 'filename'},
            'datetime': {'type': 'datetime', 'options': {'format': '%A %B %Y at %X'}}
        }
        add._write_file('_template/test.md',
                        'docs/testsample.md',
                        config,
                        'testsample')

        expect = """testsample created at {0}""".format((datetime.now()).strftime('%A %B %Y at %X'))
        self.assertEqual(expect, io.open('docs/testsample.md', 'r').read())

    # Parse keyword
    def test_parse_keyword(self):
        config = {'type': 'date'}
        self.assertEqual(add._parse_keyword(config, None), (date.today().strftime('%x')))

        config = {'type': 'date', 'options': {'format': '%A %B %Y'}}
        self.assertEqual(add._parse_keyword(config, None), (date.today().strftime('%A %B %Y')))

        config = {'type': 'datetime'}
        self.assertEqual(add._parse_keyword(config, None), (datetime.now()).strftime('%c'))

        config = {'type': 'datetime', 'options': {'format': '%A %B %Y at %X'}}
        self.assertEqual(add._parse_keyword(config, None),
                         (datetime.now()).strftime('%A %B %Y at %X'))

        config = {'type': 'filename'}
        filename = "Testfile"
        self.assertEqual(add._parse_keyword(config, filename), filename)

        config = {'type': 'text', 'value': 'A test text'}
        self.assertEqual(add._parse_keyword(config, None), 'A test text')

        config = {'type': 'testtype'}
        self.assertEqual(add._parse_keyword(config, None), 'Not a usable type')
