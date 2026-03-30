-- Рядки для лінійного графіка (день + значення). Замініть на агрегацію з ваших таблиць.
SELECT * FROM VALUES
  ('Пн', CAST(1620 AS INT)),
  ('Вт', CAST(1750 AS INT)),
  ('Ср', CAST(1690 AS INT)),
  ('Чт', CAST(1820 AS INT)),
  ('Пт', CAST(2100 AS INT)),
  ('Сб', CAST(2340 AS INT)),
  ('Нд', CAST(1980 AS INT))
AS weekly(day_label, orders)
