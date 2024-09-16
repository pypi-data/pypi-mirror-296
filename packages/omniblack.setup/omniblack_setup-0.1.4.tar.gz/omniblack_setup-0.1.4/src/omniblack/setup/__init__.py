from contextlib import suppress
from json import dumps
from os.path import splitext, dirname
from distutils.core import run_setup
from distutils.unixccompiler import UnixCCompiler
from logging import getLogger
from os import path

from setuptools.command.build_ext import build_ext
from msgspec.json import encode, format
from ruamel.yaml import YAML

from .gcc import parse_command


def write_package_config(cmd, basename, filename):
    yaml = YAML()

    with suppress(FileNotFoundError):
        with open('package_config.yaml') as file:
            value = yaml.load(file)

        argname = splitext(basename)[0]

        str_value = dumps(value, separators=(',', ':'), ensure_ascii=False)

        cmd.write_or_delete_file(argname, filename, str_value)


def write_external_requires(cmd, basename, filename):
    externals = getattr(cmd.distribution, 'requires_external', None) or []

    externals = '\n'.join(externals)

    argname = splitext(basename)[0]

    cmd.write_or_delete_file(argname, filename, externals)


def get_compiler_commands(pkg_dir):
    cmds = []

    class Compiler(UnixCCompiler):
        def spawn(self, cmd, **kwargs):
            cmds.append(tuple(cmd))

    class Command(build_ext):
        def build_extensions(self):
            self.compiler.__class__ = Compiler
            return super().build_extensions()

    dist = get_dist(path.join(pkg_dir, 'setup.py'))
    dist.cmdclass['build_ext'] = Command

    dist.run_command('build_ext')

    return [
        parse_command(pkg_dir, cmd)
        for cmd in cmds
    ]


def write_compile_commands(__file__):
    pkg_dir = dirname(__file__)
    cmds = get_compiler_commands(pkg_dir)
    buffer = encode([
        cmd
        for cmd in cmds
        if cmd.file is not None
    ])
    with open(path.join(pkg_dir, 'compile_commands.json'), 'wb') as file:
        buffer = format(buffer, indent=4)
        file.write(buffer)


def get_dist(setup_file_path):
    log = getLogger()
    log.disabled = True
    return run_setup(setup_file_path, stop_after='commandline')
