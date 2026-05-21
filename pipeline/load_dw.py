from logger import setup_logging
from rappi_parser import parse

setup_logging()
parse("bronze/rappi.json")
