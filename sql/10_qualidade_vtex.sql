-- Pergunta: quantos SKUs ativos da VTEX têm campos essenciais vazios?
-- SUM(CASE WHEN ... THEN 1 ELSE 0 END) é um contador condicional.
SELECT COUNT(*) AS total_sku,
       SUM(CASE WHEN marca          IS NULL THEN 1 ELSE 0 END) AS sem_marca,
       SUM(CASE WHEN meta_descricao IS NULL THEN 1 ELSE 0 END) AS sem_meta_descricao,
       SUM(CASE WHEN titulo_pagina  IS NULL THEN 1 ELSE 0 END) AS sem_titulo_pagina,
       SUM(CASE WHEN descricao      IS NULL THEN 1 ELSE 0 END) AS sem_descricao,
       SUM(CASE WHEN ean            IS NULL THEN 1 ELSE 0 END) AS sem_ean,
       SUM(CASE WHEN depto          IS NULL THEN 1 ELSE 0 END) AS sem_departamento
FROM vtex
WHERE sku_ativo;
