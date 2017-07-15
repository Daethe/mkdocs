# coding: utf-8
from __future__ import unicode_literals

import io
import logging
import os

config_text = 'site_name: My Docs\n'
index_text = """# Welcome to MkDocs

For full documentation visit [mkdocs.org](http://mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
"""
template_config_text = """# For each template you can use type:
#    - filename
#    - datetime
#    - date
#    - text
# With 'datetime' and 'date' type you can use as option:
#    - format

sample:
  filename:
    type: filename
  datetime:
    type: datetime
  datetime_format:
    type: datetime
    options:
      format: '%A %B %Y at %X'
  date:
    type: date
  date_format:
    type: date
    options:
      format: '%x'
  text:
    type: text
    value: "Lorem ipsum dolor sit amet"
"""
template_sample_text = """The filename: {{filename}}
The datetime: {{datetime}}
The formatted datetime: {{datetime_format}}
The date: {{date}}
The formatted date: {{date_format}}
The text: {{text}}
"""

log = logging.getLogger(__name__)


def new(output_dir, template_dir_name):

    docs_dir = os.path.join(output_dir, 'docs')
    config_path = os.path.join(output_dir, 'mkdocs.yml')
    index_path = os.path.join(docs_dir, 'index.md')

    if template_dir_name is not None:
        template_dir = os.path.join(output_dir, template_dir_name)
    else:
        template_dir = os.path.join(output_dir, '_template')
    template_config_path = os.path.join(template_dir, '_config.yml')
    template_sample_path = os.path.join(template_dir, 'sample.md')

    if os.path.exists(config_path):
        log.info('Project already exists.')
        return

    if not os.path.exists(output_dir):
        log.info('Creating project directory: %s', output_dir)
        os.mkdir(output_dir)

    log.info('Writing config file: %s', config_path)
    io.open(config_path, 'w', encoding='utf-8').write(config_text)

    if os.path.exists(index_path):
        return

    log.info('Writing initial docs: %s', index_path)
    if not os.path.exists(docs_dir):
        os.mkdir(docs_dir)
    io.open(index_path, 'w', encoding='utf-8').write(index_text)

    if not os.path.exists(template_dir):
        log.info('Creating template directory: %s', template_dir)
        os.mkdir(template_dir)

    log.info('Writing template config file: %s', template_config_path)
    io.open(template_config_path, 'w', encoding='utf-8').write(template_config_text)

    log.info('Writing sample template file: %s', template_sample_path)
    io.open(template_sample_path, 'w', encoding='utf-8').write(template_sample_text)
