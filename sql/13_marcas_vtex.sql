-- Pergunta: como o catálogo se distribui por marca na VTEX?
SELECT marca, COUNT(*) AS qtd
FROM vtex
GROUP BY marca
ORDER BY qtd DESC;
