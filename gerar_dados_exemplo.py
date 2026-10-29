"""Gera planilhas FICTÍCIAS com o mesmo layout do Radar e da VTEX (para o repositório rodar sem dados reais)."""
from pathlib import Path
import pandas as pd

pasta = Path(__file__).parent / "dados_exemplo"
pasta.mkdir(exist_ok=True)

cols_erp = ["Código", "Nome Produto", "Código GTIN", "Class. Fiscal", "Marca Comercial", "Peso Bruto",
            "Inativo", "Código Produto Kit", "Quantidade Kit", "Nome Produto Kit",
            "Dimensão Largura", "Dimensão Altura", "Dimensão Comprimento", "Descrição"]
erp = pd.DataFrame([
    ["P001", "Camera de trilha A", "7890000000011", "85258999", "Marca Unica", "0,500", "Não", None, None, None, "10", "5", "8", "Descrição A"],
    ["P002", "Cartao de memoria", "7890000000028", "85234999", "Marca Unica", "0,010", "Não", None, None, None, "3", "1", "2", "Descrição B"],
    ["P003", "Kit camera + cartao", "7890000000035", "85258999", "Marca Unica", "0,600", "Não", "P001", "1", "Camera de trilha A", "12", "8", "10", "Descrição C"],
    ["P003", "Kit camera + cartao", "7890000000035", "85258999", "Marca Unica", "0,600", "Não", "P002", "2", "Cartao de memoria", "12", "8", "10", "Descrição C"],
    ["P004", "Microscopio digital", "7890000000042", "90118000", "Marca Unica", "1,200", "Não", None, None, None, "15", "20", "25", "Descrição D"],
    ["P005", "Produto so no ERP", "7890000000059", "85258999", "Marca Unica", "0,300", "Não", None, None, None, "5", "5", "5", "Descrição E"],
], columns=cols_erp)

cols_vtex = ["ID do produto", "Nome do produto", "Produto ativo", "Descrição", "Descrição adicional", "ID da marca",
             "Marca", "ID do departamento", "Departamento", "Políticas comerciais", "URL do produto",
             "Título da página", "Meta descrição", "Mostrar no site", "Mostrar quando estiver fora de estoque",
             "Código de referência do produto", "Código fiscal", "ID do SKU", "Nome do SKU", "SKU ativo", "Kit",
             "EAN/UPC", "Código do fabricante", "Peso do pacote", "Largura do pacote", "Altura do pacote",
             "Comprimento do pacote", "Peso real", "Unidade de medida", "Condição comercial"]


def sku(ref, idsku, marca, kit, ean, peso, larg, meta, ncm="85258999"):
    d = dict.fromkeys(cols_vtex)
    d.update({"ID do produto": ref, "Nome do produto": f"Produto {ref}", "Produto ativo": "Sim",
              "Descrição": "Texto", "Marca": marca, "Departamento": "Câmeras", "Título da página": "Titulo",
              "Meta descrição": meta, "Código de referência do produto": ref, "Código fiscal": ncm,
              "ID do SKU": idsku, "Nome do SKU": f"SKU {ref}", "SKU ativo": "Sim", "Kit": kit, "EAN/UPC": ean,
              "Peso do pacote": peso, "Largura do pacote": larg, "Altura do pacote": "5",
              "Comprimento do pacote": "8"})
    return d


vtex = pd.DataFrame([
    sku("P001", "1", "Intelbras", "Não", "7890000000011", "500", "10", "Meta ok"),
    sku("P002", "2", "INTELBRAS", "Não", "7890000000028", "10", "3", None, "85234999"),
    sku("P003", "3", "Intelbrás", "Não", "7890000000035", "620", "12", "Meta ok"),  # kit sem flag
    sku("P004", "4", None, "Não", "7890000009999", "1200", "15", "Meta ok", "90118000"),
    sku("P099", "9", "Outra Marca", "Não", "7890000000099", "100", "4", "Meta ok"),
], columns=cols_vtex)

erp.to_excel(pasta / "radar_exemplo.xlsx", index=False)
vtex.to_excel(pasta / "vtex_exemplo.xlsx", index=False)
print("Dados de exemplo gerados em", pasta)
