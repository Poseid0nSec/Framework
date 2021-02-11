import argparse
import logging
from colorama import init, Fore
from modules import *

init()
logging.addLevelName(logging.INFO, f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}")
logging.addLevelName(logging.DEBUG, f"{Fore.LIGHTCYAN_EX}[*]{Fore.RESET}")
logging.addLevelName(logging.WARNING, f"{Fore.YELLOW}[!]{Fore.RESET}")
logging.addLevelName(logging.CRITICAL, f"{Fore.RED}[!!]{Fore.RESET}")
logging.basicConfig(format=f"{Fore.LIGHTBLACK_EX}[%(asctime)s]%(levelname)s%(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.DEBUG
                    )

parser = argparse.ArgumentParser(
    description="Pentest Framework v1.0.0"
)

# Framework options
f_group = parser.add_argument_group("Framework", "Options for framework")
f_group.add_argument("-v", "--version", help="Shows framework version", action="count")

modules = [module(parser) for module in module.Module.__subclasses__()]
args = parser.parse_args()

for module_ in modules:
    if vars(args)[module_.optname] == True:
        module_.initialize(vars(args))