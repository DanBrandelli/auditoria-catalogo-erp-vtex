-- Pergunta: quais são os kits do ERP, com quantos componentes e quantas peças no total?
-- n_componentes e total_pecas vêm do agrupamento feito no Python (uma linha por componente no Radar).
SELECT codigo, nome, n_componentes, total_pecas
FROM erp
WHERE eh_kit
ORDER BY total_pecas DESC;
