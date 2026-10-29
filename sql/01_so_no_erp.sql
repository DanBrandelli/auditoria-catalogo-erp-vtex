-- Pergunta: quais produtos ativos existem no ERP mas não foram cadastrados na VTEX?
-- LEFT JOIN mantém todo o ERP; onde não há par na VTEX, v.refid vem NULL.
SELECT e.codigo, e.nome
FROM erp e
LEFT JOIN vtex v ON e.codigo = v.refid
WHERE v.refid IS NULL
  AND NOT e.inativo;
