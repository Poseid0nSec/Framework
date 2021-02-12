import logging
import argparse


class Module:
    name = "Module Name"
    optname = "module"  # Option to load module
    desc = "Module Description"
    version = "1.0"

    def __init__(self, parser: argparse.ArgumentParser):
        self.arguments = {}

        self.module_group = parser.add_argument_group(self.name, self.desc)
        self.module_group.add_argument(f"--{self.optname}", action="store_true", help=f"Load module {self.name}")
        self.options(self.module_group)

    def initialize(self, options: dict):
        '''Called when module is enabled'''
        self.arguments = options

        if options[self.optname]:
            logging.info(f"{self.name} module enabled!")

    def on_shutdown(self):
        '''Called when shutting down'''
        pass

    def options(self, parser):
        '''Add module options to parser'''
        pass
