-- Pergunta: largura, altura ou comprimento divergem além da tolerância?
SELECT e.codigo, e.nome,
       e.largura AS larg_erp, v.largura AS larg_vtex,
       e.altura AS alt_erp, v.altura AS alt_vtex,
       e.comprimento AS comp_erp, v.comprimento AS comp_vtex
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE (e.largura IS NOT NULL AND v.largura IS NOT NULL
         AND ABS(e.largura - v.largura) / NULLIF(v.largura, 0) > $tol)
   OR (e.altura IS NOT NULL AND v.altura IS NOT NULL
         AND ABS(e.altura - v.altura) / NULLIF(v.altura, 0) > $tol)
   OR (e.comprimento IS NOT NULL AND v.comprimento IS NOT NULL
         AND ABS(e.comprimento - v.comprimento) / NULLIF(v.comprimento, 0) > $tol);
