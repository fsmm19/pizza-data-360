- Fuente A: Rappi (JSON) 
  ```json
  {
    "order_id": "R102",
    "item": "Pizz_Pepp_Med",
    "qty": 2,
    "price": "35000",
    "ts": 1715637600 
  }
  ```

- Fuente B: UberEats (CSV)
  ```csv
  "2026/05/13","Mediana Pepperoni","1","35000.00","UberEats_Bog"
  ```

- Fuente C: POS Local (Relacional)
  ```sql
  INSERT INTO Ventas (SKU, Cantidad, Precio, Fecha) VALUES ('SKU-992-P', 5, 35000, '2026-05-13');
  ```

---

# Fact Table de ventas

```
Fact_Ventas
├── order_id (PK)
├── date_key (FK → Dim_Fecha)
├── product_key (FK → Dim_Producto)
├── channel_key (FK → Dim_Canal)
├── quantity
├── unit_price
├── total_price
└── time_precision
```