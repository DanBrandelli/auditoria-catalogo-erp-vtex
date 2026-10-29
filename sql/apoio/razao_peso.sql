-- Apoio: razão entre o peso da VTEX e o do ERP, para conferir a unidade (kg x g).
SELECT v.peso / NULLIF(e.peso, 0) AS razao
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.peso > 0 AND v.peso > 0;
