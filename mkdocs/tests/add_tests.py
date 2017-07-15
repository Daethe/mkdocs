#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from os import chdir, mkdir, rmdir
import io
import unittest
import tempfile
from datetime import datetime, date

from mkdocs.commands import add, new


class AddTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tempdir = tempfile.mkdtemp()
        chdir(tempdir)
        new.new("testproject", None)
        chdir("testproject")

    # Is current working directory a mkdocs project
    def test_is_cwd_mkdocs_project(self):
        """Current directory is a mkdocs project"""
        self.assertTrue(add._is_cwd_mkdocs_project())

    # Is current working directory as a template directory
    def test_is_cwd_as_template_directory(self):
        """Current directory as a template directory or not"""
        self.assertTrue(add._is_cwd_as_template_directory('_template'))
        self.assertFalse(add._is_cwd_as_template_directory('dir_error'))

    # As template in template directory
    def test_as_template_in_template_directory(self):
        """As or not the template file in directory"""
        self.assertTrue(add._as_template_in_template_directory('_template/sample.md'))
        self.assertFalse(add._as_template_in_template_directory('_template/test.md'))

    # As config in template directory
    def test_as_config_in_template_directory(self):
        """As the config file in directory"""
        self.assertTrue(add._as_config_in_template_directory('_template'))
        self.assertFalse(add._as_config_in_template_directory('_test'))
        self.assertFalse(add._as_not_file_in_docs_directory('docs/index.md'))
        self.assertTrue(add._as_not_file_in_docs_directory('no_file_in_dir'))

    # As output directory
    def test_as_output_directory(self):
        """Output directory already exist"""
        mkdir('docs/output')
        self.assertTrue(add._as_output_directory('docs/output', False))
        rmdir('docs/output')
        self.assertFalse(add._as_output_directory('output', False))
        self.assertTrue(add._as_output_directory('docs/output', True))

    # Get config file
    def test_get_config_file_with_undefined_name(self):
        """Undefined name, not in config file"""
        self.assertEqual(add._get_config_file('_template', 'undefined'), None)

    # Check existance
    def test_check_existance(self):
        """Everything is ok and exist"""
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
    @unittest.skip("Need to do some search")
    def test_write_file(self):
        """File value is template parsed value"""
        config = {
            'filename': {'type': 'filename'},
            'datetime': {'type': 'datetime'},
            'datetime_format': {'type': 'datetime', 'options': {'format': '%A %B %Y at %X'}},
            'date': {'type': 'date'},
            'date_format': {'type': 'date', 'options': {'format': '%A %B %Y'}},
            'text': {'type': 'text', 'value': 'Lorem ipsum dolor sit amet'}
        }
        add._write_file('_template/sample.md',
                        'docs/testsample.md',
                        config,
                        'testsample')

        expect = format("""The filename: testsample
        The datetime: %s
        The formatted datetime: %s
        The date: %s
        The formatted date: %s
        The text: Lorem ipsum dolor sit amet""",
                        (datetime.now()).strftime('%c'),
                        (datetime.now()).strftime('%A %B %Y at %X'),
                        (date.today()).strftime('%x'),
                        (date.today()).strftime('%A %B %Y'))
        self.assertEqual(expect, io.open('docs/testsample.md', 'r').read())

    # Parse keyword
    def test_parse_keyword(self):
        """Parse variable"""
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
