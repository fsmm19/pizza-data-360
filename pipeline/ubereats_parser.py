import logging, csv
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
    try:
        with open(filepath) as file:
            orders = csv.DictReader(
                file,
                fieldnames=[
                    "date",
                    "product_name",
                    "quantity",
                    "unit_price",
                    "channel",
                ],
            )
            return list(orders)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None


def _transform(orders: list[dict]) -> list[dict]:
    valid_orders = []

    for index, order in enumerate(orders):
        if len(order.keys()) != ORDER_ROW_LENGTH:
            logger.warning(
                f"Order with unexpected number of rows: {len(order.keys())}. Order data: {order}"
            )
            continue

        is_valid = True
        transformed_order = {}

        for key, value in order.items():
            match key:
                case "date":
                    try:
                        transformed_order["ordered_at"] = datetime.strptime(
                            value, "%Y/%m/%d"
                        )
                    except ValueError:
                        logger.warning(
                            f"Invalid date format: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                case "product_name":
                    transformed_order["source_id"] = value
                case "quantity":
                    try:
                        transformed_order[key] = int(value)
                        if transformed_order[key] < 0:
                            logger.warning(
                                f"Negative quantity value: {value}. Order data: {order}"
                            )
                            is_valid = False
                            break
                    except ValueError:
                        logger.warning(
                            f"Invalid quantity format: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                case "unit_price":
                    try:
                        transformed_order[key] = float(value.replace(",", ""))
                        if transformed_order[key] < 0:
                            logger.warning(
                                f"Negative unit_price value: {value}. Order data: {order}"
                            )
                            is_valid = False
                            break
                    except ValueError:
                        logger.warning(
                            f"Invalid price format: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                case "channel":
                    transformed_order["source"] = "ubereats"

        if not is_valid:
            continue

        transformed_order["time_precision"] = "date_only"
        transformed_order["raw_id"] = f"U-{index}"
        valid_orders.append(transformed_order)

    return valid_orders
