import logging, csv

logger = logging.getLogger(f"pipeline.{__name__}")


def load_mapping_table(filepath: str) -> dict | None:
    try:
        with open(filepath) as file:
            products = csv.DictReader(file)

            return {
                product["source_id"]: {
                    "canonical_product_id": product["canonical_product_id"],
                    "canonical_name": product["canonical_name"],
                }
                for product in products
            }
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None


def transform(orders: list[dict], mapping: dict) -> tuple[list[dict], list[dict]]:
    resolved = []
    orders_unresolved = []

    for order in orders:
        source_id = mapping.get(order["source_id"])

        if source_id:
            order["canonical_product_id"] = source_id["canonical_product_id"]
            order["total_price"] = order["quantity"] * order["unit_price"]
            order["ordered_at"] = order["ordered_at"].isoformat()
            del order["source_id"]
            resolved.append(order)
        else:
            logger.warning(
                f"Product with source_id {order['source_id']} not found in mapping table. Order data: {order}"
            )
            order["ordered_at"] = order["ordered_at"].isoformat()
            orders_unresolved.append(order)

    return resolved, orders_unresolved
