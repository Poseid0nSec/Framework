from modules.module import Module
import logging
import argparse


class Test(Module):
    name = "Test"
    optname = "test"
    desc = "Descricao foda"
    version = "0.3"

    def initialize(self, options: dict):
        self.arguments = options

        if options[self.optname]:
            logging.info(f"{self.name} module enabled!")

    def options(self, parser: argparse.ArgumentParser):
        parser.add_argument("-t", "--test1", action="store_true")
