-- Pergunta: há marcas escritas de formas diferentes que na prática são a mesma?
-- A "chave" remove acentos, caixa e símbolos: "Intelbras", "INTELBRAS" e "Intelbrás" viram "intelbras".
WITH base AS (
  SELECT marca,
         regexp_replace(strip_accents(lower(marca)), '[^a-z0-9]', '', 'g') AS chave
  FROM vtex
  WHERE marca IS NOT NULL
)
SELECT chave,
       COUNT(DISTINCT marca) AS variacoes,
       STRING_AGG(DISTINCT marca, ' | ') AS grafias
FROM base
GROUP BY chave
HAVING COUNT(DISTINCT marca) > 1;
