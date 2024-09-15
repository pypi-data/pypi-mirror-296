# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from xmlrpc.client import MAXINT

import humanfriendly
import pandas as pd

from nicestudio.pvetools.bases import PVECommand, MasterCommand, VirtualMachine, VM_FIELDS
from nicestudio.pvetools.utils import get_percentage


class _VmCommand(PVECommand):
    def get_vm_list(self, **options):
        pvm = self.get_pvm_api(**options)
        data_list = pvm.cluster.resources.get(type='vm')
        for data in data_list:
            yield VirtualMachine(**data)


def format_size(x):
    return humanfriendly.format_size(x)


class ListCommand(_VmCommand):
    name = "list"

    def add_arguments(self, parser: argparse.ArgumentParser):
        super().add_arguments(parser)
        parser.add_argument(
            '-f',
            '--field',
            nargs='*',
            action='extend',
            default=[],
            help='List of fields to show, default=%(default)s',
        )
        parser.add_argument(
            '--human-friendly',
            action='store_true',
            default=False,
            help='Human friendly format of sizes, default=%(default)s',
        )

    def handle(self, *args, **options):
        vm_list = list(self.get_vm_list(**options))
        df = pd.DataFrame(vm_list)
        fields = options.get('field', None) or []
        if fields:
            df = df[fields]
        s = df.style.hide(axis='index')
        if options.get('human_friendly') is True:
            s = s.format({
                'maxdisk': format_size,
                'disk': format_size,
                'maxmem': format_size,
                'mem': format_size,
                'diskwrite': format_size,
                'diskread': format_size,
                'netout': format_size,
                'netin': format_size,
            })
        self.stdout.write(s.to_string(delimiter='\t'))


class TopCommand(_VmCommand):
    name = "top"

    class ItemValue:
        def __init__(self, total=0, usage=0):
            self.total = total
            self.usage = usage

        def get_percentage(self):
            return get_percentage(self.usage, self.total)

    class HeaderItem:
        def __init__(self, title):
            self.title = title
            self.all = TopCommand.ItemValue()
            self.data = {}

        def add(self, status, total, usage):
            value = self.data.get(status, TopCommand.ItemValue())
            value.total += total
            value.usage += usage
            self.data[status] = value
            self.all.total += total
            self.all.usage += usage

        def to_string(self):
            items = [
                f"{v.total}/{v.usage} ({v.get_percentage()}) {s}" for s, v in self.data.items()
            ]
            output = f"{self.title}: {self.all.usage}/{self.all.total} ({self.all.get_percentage()}) total"
            if items:
                output += ", " + ", ".join(items)
            return output

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields = []
        self.order_ascending = []

    def add_arguments(self, parser: argparse.ArgumentParser):
        super().add_arguments(parser)
        parser.add_argument(
            '-f',
            '--field',
            nargs='*',
            action='extend',
            default=[],
            help='List of fields to show, default=%(default)s',
        )
        parser.add_argument(
            '-o',
            '--order',
            nargs='*',
            action='extend',
            default=[],
            help='List of order to show, default=%(default)s',
        )
        parser.add_argument(
            '-d',
            '--delay',
            type=float,
            default=5.0,
            help='Delay between showing, default=%(default)s',
        )
        parser.add_argument(
            '--human-friendly',
            action='store_true',
            default=False,
            help='Human friendly format of sizes, default=%(default)s',
        )

    def get_header(self, vm_list: list) -> list:
        vm_count = len(vm_list)
        status_count = {}
        cpu_data = TopCommand.HeaderItem("CPU")
        mem_data = TopCommand.HeaderItem("Memory")
        disk_data = TopCommand.HeaderItem("Disk")

        for vm in vm_list:
            s = vm.status
            c = status_count.get(s, 0) + 1
            status_count[s] = c
            cpu_data.add(s, vm.maxcpu, vm.cpu)
            mem_data.add(s, vm.maxmem, vm.mem)
            disk_data.add(s, vm.maxdisk, vm.disk)

        status_line = f"VM: {vm_count} totals"
        if status_count:
            items = [f"{v} ({get_percentage(v, vm_count)}) {k}" for k, v in status_count.items()]
            status_line += ", " + ", ".join(items)

        header = [
            "top - %s" % datetime.now(),
            status_line,
            cpu_data.to_string(),
            mem_data.to_string(),
            disk_data.to_string(),
        ]

        return header

    def display(self, **options):
        vm_list = list(self.get_vm_list(**options))
        header = self.get_header(vm_list)
        self.stdout.write('\n'.join(header))
        self.stdout.write('\n\n')
        self.stdout.flush()

        df = pd.DataFrame(vm_list)
        fields = options.get('field', None) or []
        if fields:
            df = df[fields]
        if self.order_fields:
            df = df.sort_values(self.order_fields, ascending=self.order_ascending)
        s = df.style.hide(axis='index')
        if options.get('human_friendly') is True:
            s = s.format({
                'maxdisk': format_size,
                'disk': format_size,
                'maxmem': format_size,
                'mem': format_size,
                'diskwrite': format_size,
                'diskread': format_size,
                'netout': format_size,
                'netin': format_size,
            })
        self.stdout.write(s.to_string(delimiter='\t'))
        self.stdout.flush()

    def handle(self, *args, **options):
        show_fields = options.get('field') or VM_FIELDS

        order_fields = []
        order_ascending = []
        for f in options.get('order', []):
            if f.startswith('+'):
                is_ascending = True
                f = f[1:]
            else:
                is_ascending = False
            if f not in show_fields:
                continue
            order_fields.append(f)
            order_ascending.append(is_ascending)
        self.order_fields = order_fields
        self.order_ascending = order_ascending

        self.display(**options)


class Command(MasterCommand):
    name = 'vm'

    sub_command_classes = [
        ListCommand,
        TopCommand,
    ]
