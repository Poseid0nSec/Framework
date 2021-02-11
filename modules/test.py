from modules.module import Module
import logging

class Test(Module):
    name = "Test"
    optname = "test"
    desc = "Descricao foda"
    version = "0.3"

    def initialize(self, options: dict):
        self.arguments = options

        if options["test"]:
            logging.info("Test module enabled!")