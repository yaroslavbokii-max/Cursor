-- Сегменти для doughnut. Замініть на розбивку з ваших даних.
SELECT * FROM VALUES
  ('Food', CAST(62 AS INT)),
  ('Store', CAST(28 AS INT)),
  ('Інше', CAST(10 AS INT))
AS pie(label, pct)
