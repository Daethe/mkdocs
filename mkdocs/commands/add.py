# coding: utf-8

from __future__ import unicode_literals
import io
import logging
import re
from datetime import datetime, date
from os import getcwd, mkdir
from os.path import join, exists, isfile
import yaml


# Define some directory
scaffold_dir = join(getcwd(), '_scaffold')
config_path = join(getcwd(), 'mkdocs.yml')

# Get log object
log = logging.getLogger(__name__)


def _is_cwd_mkdocs_project():
    if not exists(config_path):
        log.error('This is not a mkdocs projet directory.')
        return False
    return True


def _is_cwd_as_template_directory(directory):
    if not exists(directory):
        log.error('There is no template directory.')
        return False
    return True


def _as_template_in_template_directory(path):
    if not isfile(path):
        log.error('This template doesn\'t exist. You need to create it first.')
        return False
    return True


def _as_config_in_template_directory(tpl_dir):
    if not isfile(join(tpl_dir, '_config.yml')):
        log.error('_config.yml is missing in template directory')
        return False
    return True


def _as_output_directory(directory, create):
    if not exists(directory) and not create:
        log.error('Output directory doesn\'t exist. You need to create it first.')
        return False
    elif not exists(directory) and create:
        mkdir(directory)
    return True


def _as_not_file_in_docs_directory(path):
    if isfile(path):
        log.error('This file already exist.')
        return False
    return True


def add(tpl_name, output_dir, filename, create_dir, tpl_dir):
    """
        Add a new page with scaffolded template
    """

    # Check if directory is a mkdocs project
    if _is_cwd_mkdocs_project():

        # Set template directory following parameter
        if tpl_dir is not None:
            tpl_dir = join(getcwd(), tpl_dir)
        else:
            tpl_dir = scaffold_dir
        tpl_path = join(tpl_dir, str(tpl_name) + '.md')
        output_dir = join('docs', output_dir)
        file_path = join(output_dir, str(filename) + '.md')

        if __check_existance(tpl_dir, tpl_path, output_dir, file_path, create_dir):
            __write_file(tpl_path, file_path, __get_config_file(tpl_dir, tpl_name), filename)
            log.info('The file was successfully created in ' + file_path)

    return


def __get_config_file(tpl_dir, tpl_name):
    data = yaml.load(
        io.open(join(tpl_dir, '_config.yml'), 'r')
    )
    if data.has_key(tpl_name):
        return data[tpl_name]
    return None

def __check_existance(tpl_dir, tpl_path, output_dir, file_path, create_dir):
    """
        Check existance or not of folder/file
    """
    everything_is_ok = True and (
        _is_cwd_as_template_directory(tpl_dir) and
        _as_template_in_template_directory(tpl_path) and
        _as_config_in_template_directory(tpl_dir) and
        _as_output_directory(output_dir, create_dir) and
        _as_not_file_in_docs_directory(file_path)
    )

    return everything_is_ok


def __write_file(tpl_path, file_path, tpl_config, filename):
    """
        Write template content to file
    """
    tpl_value = io.open(tpl_path, 'r', encoding='utf-8').read()

    # Test it
    if not tpl_config is None:
        var_lists = re.findall(r'{{[A-Za-z0-9\-\_]+}}', tpl_value)
        for var in var_lists:
            var_value = __parse_keyword(tpl_config, var[2:-2], filename)
            tpl_value = re.sub(var, var_value, tpl_value)
    # End Test

    io.open(file_path, 'w', encoding='utf-8').write(tpl_value)
    return


def __parse_keyword(tpl_config, var_config, filename):
    keywords = ['filename', 'datetime', 'date']

    if tpl_config[var_config] in keywords:
        if tpl_config[var_config] == 'filename':
            return filename
        if tpl_config[var_config] == 'datetime':
            return str(datetime.now())
        if tpl_config[var_config] == 'date':
            return str(date.today())

    return tpl_config[var_config]
            