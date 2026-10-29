-- Pergunta: o que é kit no ERP também está marcado como kit na VTEX (e vice-versa)?
SELECT e.codigo, e.nome,
       e.eh_kit AS kit_no_erp, v.kit AS kit_na_vtex,
       e.n_componentes, e.total_pecas
FROM erp e
JOIN vtex v ON e.codigo = v.refid
WHERE e.eh_kit <> v.kit;
