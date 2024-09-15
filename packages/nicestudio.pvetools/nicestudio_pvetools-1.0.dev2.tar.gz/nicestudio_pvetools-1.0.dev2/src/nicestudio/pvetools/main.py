# -*- coding: utf-8 -*-
import argparse
import sys

from nicestudio.pvetools.bases import MasterCommand
from nicestudio.pvetools.commands import vm


class MainCommand(MasterCommand):
    sub_command_classes = [
        vm.Command,
    ]

    def __init__(self, *args, **kwargs):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        super().__init__(*args, **kwargs)
        self.options = None

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--host',
            help='Hostname or IP address of PVE Server, default=%(default)s',
        )
        parser.add_argument(
            '--user',
            help='Username to use when connecting to PVE Server, default=%(default)s',
        )
        parser.add_argument(
            '--password',
            help='Password to use when connecting to PVE Server, default=%(default)s',
        )
        super().add_arguments(parser)

    def execute(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)
        self.options = parser.parse_args()
        options = vars(self.options)
        func = getattr(self.options, 'func', None) or self.handle
        if func:
            ret = func(**options)
            self.stdout.flush()
            self.stderr.flush()
            return ret


def main():
    MainCommand.execute()
