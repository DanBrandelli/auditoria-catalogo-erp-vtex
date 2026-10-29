-- Pergunta: o peso diverge além da tolerância ($tol = diferença relativa aceita)?
-- NULLIF evita divisão por zero. Confira a unidade (kg x g) antes de interpretar.
SELECT e.codigo, e.nome, e.peso AS peso_erp, v.peso AS peso_vtex
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.peso IS NOT NULL
  AND v.peso IS NOT NULL
  AND ABS(e.peso - v.peso) / NULLIF(v.peso, 0) > $tol;
