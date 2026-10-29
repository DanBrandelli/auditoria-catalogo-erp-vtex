-- Pergunta: o código de barras (GTIN no ERP, EAN na VTEX) é o mesmo nos dois sistemas?
-- IS DISTINCT FROM trata NULL como valor: "tem código de um lado e vazio do outro" também é divergência.
SELECT e.codigo, e.nome, e.gtin AS gtin_erp, v.ean AS ean_vtex
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.gtin IS DISTINCT FROM v.ean;
