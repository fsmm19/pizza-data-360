from logger import setup_logging

# from rappi_parser import _load, _transform
# from ubereats_parser import _load
from pos_parser import _load

setup_logging()
# orders = _load("bronze/rappi.json")
# _transform(orders)

print(_load("bronze/pos.db"))
