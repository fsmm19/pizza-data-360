import logging, sqlite3
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
ORDER_ROW_LENGTH = 5


def parse(filepath: str):
    orders = _load(filepath)

    if orders is None:
        return []

    if not len(orders):
        logger.warning(f"No orders found in file: {filepath}")
        return orders

    valid_orders = _transform(orders)
    logger.info(f"Parsed {len(valid_orders)} valid orders from file: {filepath}")
    return valid_orders


def _load(filepath: str) -> list[dict] | None:
    if not Path(filepath).exists():
        logger.error(f"File not found: {filepath}")
        return None

    try:
        with sqlite3.connect(filepath) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM ventas")

            orders = [dict(row) for row in cursor.fetchall()]
            return orders
    except sqlite3.OperationalError as e:
        logger.error(f"Database error: {e}. File: {filepath}")
        return None


def _transform(orders: list[dict]) -> list[dict]:
    valid_orders = []

    for order in orders:
        if len(order.keys()) != ORDER_ROW_LENGTH:
            logger.warning(
                f"Order with unexpected number of rows: {len(order.keys())}. Order data: {order}"
            )
            continue

        is_valid = True
        transformed_order = {}

        for key, value in order.items():
            match key:
                case "id":
                    transformed_order["raw_id"] = f"P-{value}"
                case "sku":
                    transformed_order["source_id"] = value
                case "quantity":
                    if value < 0:
                        logger.warning(
                            f"Negative quantity value: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order[key] = value
                case "unit_price":
                    if value < 0:
                        logger.warning(
                            f"Negative unit_price value: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order[key] = value
                case "date":
                    try:
                        transformed_order["ordered_at"] = datetime.strptime(
                            value, "%Y-%m-%d"
                        )
                    except ValueError:
                        logger.warning(
                            f"Invalid date format: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break

        if not is_valid:
            continue

        transformed_order["time_precision"] = "date_only"
        transformed_order["source"] = "pos"
        valid_orders.append(transformed_order)

    return valid_orders
