-- Pergunta: existe o mesmo EAN em mais de um SKU?
-- HAVING filtra depois do agrupamento; STRING_AGG lista os códigos envolvidos.
SELECT ean, COUNT(*) AS qtd, STRING_AGG(refid, ', ') AS codigos
FROM vtex
WHERE ean IS NOT NULL
GROUP BY ean
HAVING COUNT(*) > 1;
