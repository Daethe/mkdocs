#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import tempfile
import unittest
import os

from mkdocs.commands import new


class NewTests(unittest.TestCase):

    def test_new(self):

        tempdir = tempfile.mkdtemp()
        os.chdir(tempdir)

        new.new("myproject", None)

        expected_paths = [
            os.path.join(tempdir, "myproject"),
            os.path.join(tempdir, "myproject", "mkdocs.yml"),
            os.path.join(tempdir, "myproject", "docs"),
            os.path.join(tempdir, "myproject", "docs", "index.md"),
            os.path.join(tempdir, "myproject", "_template"),
            os.path.join(tempdir, "myproject", "_template", "_config.yml"),
            os.path.join(tempdir, "myproject", "_template", "sample.md")
        ]

        for expected_path in expected_paths:
            self.assertTrue(os.path.exists(expected_path))
