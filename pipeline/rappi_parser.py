import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(f"pipeline.{__name__}")
ORDER_KEYS_LENGTH = 5


def parse(filepath: str) -> list[dict]:
    try:
        with open(filepath) as file:
            orders = json.load(file)
            transform(orders)
            return orders
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return []
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {filepath}")
        return []


def transform(orders: list[dict]) -> list[dict]:
    for order in orders:
        if len(order.keys()) != ORDER_KEYS_LENGTH:
            logger.warning(
                f"Order with unexpected number of keys: {len(order.keys())}. Order data: {order}"
            )
            break

        for key, value in order.items():
            match key:
                case "order_id":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'order_id': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                    order["raw_id"] = order[key]
                    del order[key]
                    return
                case "item":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'item': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                    order["source_id"] = order[key]
                    del order[key]
                    return
                case "qty":
                    if not isinstance(value, int):
                        logger.warning(
                            f"Invalid type for 'qty': expected int, got {type(value).__name__}. Order data: {order}"
                        )
                        if value < 0:
                            logger.warning(
                                f"Negative quantity value: {value}. Order data: {order}"
                            )
                    return
                case "price":
                    if not isinstance(value, str):
                        logger.warning(
                            f"Invalid type for 'price': expected str, got {type(value).__name__}. Order data: {order}"
                        )
                        return
                    order[key] = float(value)
                    return
                case "ts":
                    if not isinstance(value, int):
                        logger.warning(
                            f"Invalid type for 'ts': expected int, got {type(value).__name__}. Order data: {order}"
                        )
                    order[key] = datetime.fromtimestamp(value, timezone.utc)
                    return
                case _:
                    logger.warning(
                        f"Unexpected key in order data: {key}. Order data: {order}"
                    )
                    return
