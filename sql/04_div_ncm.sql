-- Pergunta: a classificação fiscal (NCM) é a mesma nos dois sistemas?
SELECT e.codigo, e.nome, e.ncm AS ncm_erp, v.ncm AS ncm_vtex
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.ncm IS DISTINCT FROM v.ncm;
