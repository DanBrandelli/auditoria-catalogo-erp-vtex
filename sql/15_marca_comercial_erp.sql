-- Pergunta: o que existe no campo Marca Comercial do ERP? (se for sempre o mesmo valor, não serve de referência)
SELECT marca, COUNT(*) AS qtd
FROM erp
GROUP BY marca
ORDER BY qtd DESC;
