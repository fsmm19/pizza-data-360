import logging, json
from datetime import datetime, timezone

logger = logging.getLogger(f"pipeline.{__name__}")
ORDER_KEYS_LENGTH = 5


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
            orders = json.load(file)
            return orders
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {filepath}")
        return None


def _transform(orders: list[dict]) -> list[dict]:
    valid_orders = []

    for order in orders:
        if len(order.keys()) != ORDER_KEYS_LENGTH:
            logger.warning(
                f"Order with unexpected number of keys: {len(order.keys())}. Order data: {order}"
            )
            continue

        is_valid = True
        transformed_order = {}

        for key, value in order.items():
            match key:
                case "order_id":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'order_id': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order["raw_id"] = f"R-{value}"
                case "item":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'item': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order["source_id"] = value
                case "qty":
                    if not isinstance(value, int):
                        logger.warning(
                            f"Invalid type for 'qty': expected int, got {type(value).__name__}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    elif value < 0:
                        logger.warning(
                            f"Negative quantity value: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order["quantity"] = value
                case "price":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'price': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    try:
                        transformed_order["unit_price"] = float(value)
                        if transformed_order[key] < 0:
                            logger.warning(
                                f"Negative price value: {value}. Order data: {order}"
                            )
                            is_valid = False
                            break
                    except ValueError:
                        logger.warning(
                            f"Invalid price format: {value}. Order data: {order}"
                        )
                        is_valid = False
                        break
                case "ts":
                    if not isinstance(value, int):
                        logger.warning(
                            f"Invalid type for 'ts': expected int, got {type(value).__name__}. Order data: {order}"
                        )
                        is_valid = False
                        break
                    transformed_order["ordered_at"] = datetime.fromtimestamp(
                        value, timezone.utc
                    )
                case _:
                    logger.warning(
                        f"Unexpected key in order data: {key}. Order data: {order}"
                    )
                    is_valid = False
                    break

        if not is_valid:
            continue

        transformed_order["time_precision"] = "datetime"
        transformed_order["source"] = "rappi"
        valid_orders.append(transformed_order)

    return valid_orders
