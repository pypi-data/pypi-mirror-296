# -*- coding: utf-8 -*-
import argparse
import sys
from collections import namedtuple

from proxmoxer import ProxmoxAPI


class _Command:
    name = ""
    help = ""
    defaults = {}

    def __init__(self, *args, **kwargs):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

    def add_arguments(self, parser: argparse.ArgumentParser):
        pass

    def handle(self, *args, **options):
        raise NotImplementedError("'%s.%s' class must implement handle()" % (
            self.__class__.__module__, self.__class__.__name__))


class PVECommand(_Command):

    def get_pvm_api(self, **options):
        host = options.get('host')
        user = options.get('user')
        password = options.get('password')
        return ProxmoxAPI(host=host, user=user, password=password)


class MasterCommand(_Command):
    sub_command_classes = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        sub_command_list = []
        for sub_command_class in self.sub_command_classes:
            sub_command = sub_command_class()
            sub_command.stdout = getattr(self, 'stdout', None)
            sub_command.stderr = getattr(self, 'stderr', None)
            sub_command_list.append(sub_command)
        self.sub_command_list = sub_command_list
        self.parser = None

    def handle(self, *args, **options):
        self.parser.print_help()

    def add_arguments(self, parser: argparse.ArgumentParser):
        super().add_arguments(parser)
        self.parser = parser

        parser.set_defaults(func=self.handle)

        sub_parsers = parser.add_subparsers(title='sub commands')
        for sub_command in self.sub_command_list:
            sub_parser = sub_parsers.add_parser(
                name=sub_command.name,
                help=sub_command.help,
            )
            sub_parser.set_defaults(func=sub_command.handle)
            sub_command.add_arguments(sub_parser)


VM_FIELDS = [
    'id',
    'type',
    'vmid',
    'node',
    'name',
    'template',
    'uptime',
    'status',
    'maxcpu',
    'cpu',
    'maxdisk',
    'disk',
    'maxmem',
    'mem',
    'diskwrite',
    'diskread',
    'netout',
    'netin',
    'tags',
]

VirtualMachine = namedtuple(
    'VirtualMachine',
    field_names=VM_FIELDS,
    defaults=[None for field in VM_FIELDS],
)
