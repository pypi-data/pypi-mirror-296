import shlex

from argparse import ArgumentParser
from msgspec import Struct


class CompileCommand(Struct):
    command: str
    arguments: list[str]
    directory: str
    output: str
    file: str


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('-f', action='append', dest='features')
    parser.add_argument('-W', action='append', dest='warnings')
    parser.add_argument('-D', action='append', dest='defines')
    parser.add_argument('-c', dest='compile_target')
    parser.add_argument('-o', dest='output')
    parser.add_argument('-I', action='append', dest='includes')
    parser.add_argument('-L', action='append', dest='link_path')
    parser.add_argument('-l', action='append', dest='link_libs')
    parser.add_argument('-shared', action='store_true', default=False)
    parser.add_argument('-pie', action='store_true', default=False)
    parser.add_argument('-std')
    parser.add_argument('files', nargs='*')

    return parser


def parse_command(directory, cmd):
    parser = get_parser()
    executable, *args = cmd
    parsed = parser.parse_args(args)

    return CompileCommand(
        command=shlex.join(cmd),
        arguments=cmd,
        output=parsed.output,
        file=parsed.compile_target,
        directory=directory,
    )
