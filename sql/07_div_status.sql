-- Pergunta: o status é coerente? ERP tem "inativo" e VTEX tem "SKU ativo" (lógica oposta).
-- Conflito = os dois verdadeiros (inativo no ERP e ativo na loja) ou os dois falsos.
SELECT e.codigo, e.nome,
       CASE WHEN e.inativo THEN 'inativo' ELSE 'ativo' END AS status_erp,
       CASE WHEN v.sku_ativo THEN 'ativo' ELSE 'inativo' END AS status_vtex
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.inativo = v.sku_ativo;
