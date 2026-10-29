-- Pergunta: quais SKUs ativos estão na loja mas não existem no ERP?
-- Espelho da consulta 01: agora o lado principal é a VTEX.
SELECT v.refid, v.id_sku, v.nome_sku
FROM vtex v
LEFT JOIN erp e ON e.codigo = v.refid
WHERE e.codigo IS NULL
  AND v.sku_ativo;
