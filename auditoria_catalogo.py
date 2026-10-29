"""
Auditoria de qualidade de catálogo: ERP (WK Radar) x VTEX

O Python prepara os dados (limpeza) e executa as consultas da pasta sql/.
Cada arquivo .sql responde uma pergunta de negócio e vira uma aba do relatório.

Uso:
    python auditoria_catalogo.py --erp radar.xlsx --vtex vtex.xlsx
    python auditoria_catalogo.py            # usa os dados de exemplo
"""
import argparse
import re
from pathlib import Path

import duckdb
import pandas as pd

BASE = Path(__file__).parent
PASTA_SQL = BASE / "sql"

COLS_ERP = {
    "Código": "codigo", "Nome Produto": "nome", "Código GTIN": "gtin",
    "Class. Fiscal": "ncm", "Marca Comercial": "marca", "Peso Bruto": "peso",
    "Inativo": "inativo", "Código Produto Kit": "kit_cod",
    "Quantidade Kit": "kit_qtd", "Nome Produto Kit": "kit_nome",
    "Dimensão Largura": "largura", "Dimensão Altura": "altura",
    "Dimensão Comprimento": "comprimento", "Descrição": "descricao",
}
COLS_VTEX = {
    "ID do produto": "id_produto", "Nome do produto": "nome",
    "Produto ativo": "produto_ativo", "Descrição": "descricao",
    "Marca": "marca", "Departamento": "depto",
    "Título da página": "titulo_pagina", "Meta descrição": "meta_descricao",
    "Código de referência do produto": "refid", "Código fiscal": "ncm",
    "ID do SKU": "id_sku", "Nome do SKU": "nome_sku", "SKU ativo": "sku_ativo",
    "Kit": "kit", "EAN/UPC": "ean", "Peso do pacote": "peso",
    "Largura do pacote": "largura", "Altura do pacote": "altura",
    "Comprimento do pacote": "comprimento",
}


# ----------------------------------------------------------------------
# Limpeza
# ----------------------------------------------------------------------
def ler(caminho, mapa):
    caminho = str(caminho)
    if caminho.lower().endswith(".csv"):
        df = pd.read_csv(caminho, dtype=str, sep=None, engine="python")
    else:
        df = pd.read_excel(caminho, dtype=str)
    faltando = [c for c in mapa if c not in df.columns]
    if faltando:
        raise SystemExit(f"Colunas não encontradas em {caminho}: {faltando}")
    return df[list(mapa)].rename(columns=mapa)


def txt(s):
    s = s.astype("string").str.strip()
    return s.mask(s == "")


def so_digitos(s):
    s = txt(s).str.replace(r"\D", "", regex=True)
    return s.mask(s == "")


def num(s):
    """Converte número em formato BR ('1.234,5') ou US ('1234.5') para float."""
    s = txt(s)
    tem_virgula = s.str.contains(",", na=False)
    s = s.where(~tem_virgula,
                s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(s, errors="coerce")


def sim(s):
    return txt(s).str.lower().isin(["sim", "true", "1", "yes", "verdadeiro", "s", "x"])


def preparar_erp(caminho, fator_peso):
    df = ler(caminho, COLS_ERP)
    for c in ["codigo", "nome", "marca", "kit_cod", "kit_nome", "descricao"]:
        df[c] = txt(df[c])
    df["gtin"] = so_digitos(df["gtin"])
    df["ncm"] = so_digitos(df["ncm"])
    df["inativo"] = sim(df["inativo"])
    for c in ["peso", "largura", "altura", "comprimento", "kit_qtd"]:
        df[c] = num(df[c])
    df["peso"] = df["peso"] * fator_peso

    # O Radar traz uma linha por componente de kit. Aqui volta a uma linha por produto.
    # Premissa a confirmar: "Código" = kit e "Código Produto Kit" = componente.
    erp = (df.groupby("codigo", as_index=False)
           .agg(nome=("nome", "first"), gtin=("gtin", "first"), ncm=("ncm", "first"),
                marca=("marca", "first"), peso=("peso", "first"),
                largura=("largura", "first"), altura=("altura", "first"),
                comprimento=("comprimento", "first"), descricao=("descricao", "first"),
                inativo=("inativo", "max"),
                n_componentes=("kit_cod", "nunique"),
                total_pecas=("kit_qtd", "sum")))
    erp["eh_kit"] = erp["n_componentes"] > 0
    return erp


def preparar_vtex(caminho):
    df = ler(caminho, COLS_VTEX)
    for c in ["refid", "nome", "nome_sku", "descricao", "marca", "depto",
              "titulo_pagina", "meta_descricao"]:
        df[c] = txt(df[c])
    df["ean"] = so_digitos(df["ean"])
    df["ncm"] = so_digitos(df["ncm"])
    for c in ["sku_ativo", "produto_ativo", "kit"]:
        df[c] = sim(df[c])
    for c in ["peso", "largura", "altura", "comprimento"]:
        df[c] = num(df[c])
    return df


# ----------------------------------------------------------------------
# Execução das consultas SQL
# ----------------------------------------------------------------------
def rodar_sql(con, arquivo, tolerancia):
    sql = Path(arquivo).read_text(encoding="utf-8")
    params = {"tol": tolerancia} if "$tol" in sql else None
    return con.execute(sql, params).df()


def nome_aba(arquivo):
    """'05_div_peso.sql' -> 'div_peso'"""
    return re.sub(r"^\d+_", "", Path(arquivo).stem)[:31]


def pct(a, b):
    return round(100 * float(a) / b, 1) if b else None


def main():
    ap = argparse.ArgumentParser(description="Auditoria de catálogo ERP x VTEX")
    ap.add_argument("--erp", default=BASE / "dados_exemplo" / "radar_exemplo.xlsx")
    ap.add_argument("--vtex", default=BASE / "dados_exemplo" / "vtex_exemplo.xlsx")
    ap.add_argument("--saida", default="relatorio_inconsistencias.xlsx")
    ap.add_argument("--fator-peso-erp", type=float, default=1.0,
                    help="multiplica o peso do ERP (ex.: 1000 se ERP em kg e VTEX em g)")
    ap.add_argument("--tolerancia", type=float, default=0.02,
                    help="diferença relativa aceita em peso e dimensões (padrão 2%%)")
    a = ap.parse_args()

    erp = preparar_erp(a.erp, a.fator_peso_erp)
    vtex = preparar_vtex(a.vtex)

    con = duckdb.connect()
    con.register("erp", erp)
    con.register("vtex", vtex)

    # Uma consulta por arquivo, na ordem numérica
    res = {nome_aba(f): rodar_sql(con, f, a.tolerancia)
           for f in sorted(PASTA_SQL.glob("*.sql"))}

    n_erp = int((~erp["inativo"]).sum())
    n_vtex = int(vtex["sku_ativo"].sum())
    n_conc = int(rodar_sql(con, PASTA_SQL / "apoio" / "conciliados.sql", a.tolerancia)["n"][0])
    qv = res["qualidade_vtex"].iloc[0]

    def linha(rotulo, qtd, base=None):
        return (rotulo, int(qtd), pct(qtd, base) if base else None)

    resumo = pd.DataFrame([
        linha("Produtos ativos no ERP", n_erp),
        linha("SKUs ativos na VTEX", n_vtex),
        linha("Produtos ERP encontrados na VTEX", n_conc, n_erp),
        linha("Ativos no ERP e ausentes na VTEX", len(res["so_no_erp"]), n_erp),
        linha("SKUs ativos na VTEX ausentes no ERP", len(res["so_na_vtex"]), n_vtex),
        linha("Divergência GTIN/EAN", len(res["div_gtin_ean"]), n_conc),
        linha("Divergência de NCM", len(res["div_ncm"]), n_conc),
        linha("Divergência de peso", len(res["div_peso"]), n_conc),
        linha("Divergência de dimensões", len(res["div_dimensoes"]), n_conc),
        linha("Divergência de status", len(res["div_status"]), n_conc),
        linha("Divergência de kit (ERP x VTEX)", len(res["div_kit"]), n_conc),
        linha("SKUs ativos sem marca (VTEX)", qv["sem_marca"], n_vtex),
        linha("SKUs ativos sem meta descrição (VTEX)", qv["sem_meta_descricao"], n_vtex),
        linha("SKUs ativos sem EAN (VTEX)", qv["sem_ean"], n_vtex),
        linha("EANs duplicados (VTEX)", len(res["ean_duplicado"])),
        linha("Marcas com grafia duplicada (VTEX)", len(res["marcas_grafia_parecida"])),
    ], columns=["indicador", "quantidade", "percentual"])

    with pd.ExcelWriter(a.saida, engine="openpyxl") as xw:
        resumo.to_excel(xw, sheet_name="resumo", index=False)
        for nome, df in res.items():
            df.to_excel(xw, sheet_name=nome, index=False)

    print(resumo.to_string(index=False))
    razao = rodar_sql(con, PASTA_SQL / "apoio" / "razao_peso.sql", a.tolerancia)["razao"]
    if len(razao):
        print(f"\nRazão mediana peso VTEX / ERP: {razao.median():.3f} "
              "(perto de 1 = unidades compatíveis; perto de 1000 = ERP em kg e VTEX em g, "
              "use --fator-peso-erp 1000)")
    print(f"\nRelatório salvo em {a.saida}")


if __name__ == "__main__":
    main()
