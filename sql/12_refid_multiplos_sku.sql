-- Pergunta: algum código de referência tem mais de um SKU? (afeta o cruzamento com o ERP)
SELECT refid, COUNT(*) AS qtd_sku
FROM vtex
WHERE refid IS NOT NULL
GROUP BY refid
HAVING COUNT(*) > 1;
