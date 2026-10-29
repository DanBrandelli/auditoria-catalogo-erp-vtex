-- Apoio ao resumo: quantos produtos ativos do ERP foram encontrados na VTEX?
SELECT COUNT(DISTINCT e.codigo) AS n
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE NOT e.inativo;
