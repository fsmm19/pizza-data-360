import duckdb

with duckdb.connect("warehouse/warehouse.duckdb") as connection:
    print("=== Ventas totales por canal ===")
    print(connection.sql("""
        SELECT source, SUM(total_price) AS total_ventas
        FROM orders
        GROUP BY source
        ORDER BY total_ventas DESC
    """).fetchall())

    print("\n=== Ventas del producto PROD-001 ===")
    print(connection.sql("""
        SELECT canonical_product_id, SUM(total_price) AS total_ventas
        FROM orders
        WHERE canonical_product_id = 'PROD-001'
        GROUP BY canonical_product_id
    """).fetchall())

    print("\n=== Órdenes sin resolver ===")
    print(connection.sql("""
        SELECT COUNT(*) AS total_unresolved
        FROM orders_unresolved
    """).fetchall())
