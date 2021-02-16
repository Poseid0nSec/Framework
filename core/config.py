import argparse
from core import banner


def config_logging():
    import logging
    from colorama import init, Fore

    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    init()
    logging.addLevelName(logging.INFO, f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}")
    logging.addLevelName(logging.DEBUG, f"{Fore.LIGHTCYAN_EX}[*]{Fore.RESET}")
    logging.addLevelName(logging.WARNING, f"{Fore.YELLOW}[!]{Fore.RESET}")
    logging.addLevelName(logging.CRITICAL, f"{Fore.RED}[!]{Fore.RESET}")
    logging.basicConfig(format=f"{Fore.LIGHTBLACK_EX}[%(asctime)s]%(levelname)s%(message)s",
                        datefmt="%H:%M:%S",
                        level=logging.DEBUG
                        )


def set_options(parser: argparse._ArgumentGroup):
    parser.add_argument("-v", "--version", help="Shows framework version", action="store_true")


def handle_options(options: dict):
    if options["version"]:
        exit(banner.banner())


version = '1.0.0'
