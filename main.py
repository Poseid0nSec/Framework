import argparse
from core import config
from modules import *

config.config_logging()


parser = argparse.ArgumentParser(
    description=f"Pentest Framework v{config.version}",
    usage="framework.py [modules] [options]"
)

# Framework options
f_group = parser.add_argument_group("Framework", "Options for framework")
config.set_options(f_group)

# Load modules
modules = [module_(parser) for module_ in module.Module.__subclasses__()]

# Get arguments
args = parser.parse_args()

# Handle arguments
config.handle_options(vars(args))

# Run selected modules
for module_ in modules:
    if vars(args)[module_.optname]:
        module_.initialize(vars(args))
