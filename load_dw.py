import logging, sqlite3
from pathlib import Path
from pipeline.logger import setup_logging
from pipeline import rappi_parser, ubereats_parser, pos_parser
from pipeline import silver_to_gold

logger = logging.getLogger(__name__)


def load():
    setup_logging()

    mapping = silver_to_gold.load_mapping_table("mapping/products.csv")

    if mapping is None:
        logger.error("Failed to load mapping table. Exiting.")
        return

    orders = (
        rappi_parser.parse("bronze/rappi.json")
        + ubereats_parser.parse("bronze/ubereats.csv")
        + pos_parser.parse("bronze/pos.db")
    )

    resolved, unresolved = silver_to_gold.transform(orders, mapping)

    Path("warehouse").mkdir(exist_ok=True)

    with sqlite3.connect("warehouse/warehouse.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                raw_id TEXT,
                source TEXT,
                canonical_product_id TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_price REAL,
                ordered_at TEXT,
                time_precision TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_unresolved (
                raw_id TEXT,
                source TEXT,
                source_id TEXT,
                quantity INTEGER,
                unit_price REAL,
                ordered_at TEXT,
                time_precision TEXT
            )
        """)

        if resolved:
            cursor.executemany(
                """
                INSERT INTO orders (raw_id, source, canonical_product_id, quantity, unit_price, total_price, ordered_at, time_precision)
                VALUES (:raw_id, :source, :canonical_product_id, :quantity, :unit_price, :total_price, :ordered_at, :time_precision)
            """,
                resolved,
            )

        if unresolved:
            cursor.executemany(
                """
                INSERT INTO orders_unresolved (raw_id, source, source_id, quantity, unit_price, ordered_at, time_precision)
                VALUES (:raw_id, :source, :source_id, :quantity, :unit_price, :ordered_at, :time_precision)
            """,
                unresolved,
            )

        connection.commit()


if __name__ == "__main__":
    load()
