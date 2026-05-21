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

1. Unificación de Schema: Define un struct o class único para el DW.
2. Normalización de Tipos: Convierte el timestamp de Rappi, el string de Uber y el Date del POS a un solo formato de tiempo.
3. Mapeo de Atributos: Crea una tabla de equivalencias (Mapping Table) para que `"Pizz_Pepp_Med"`, `"Mediana Pepperoni"` y `"SKU-992-P"` se consoliden bajo un solo ID de producto.