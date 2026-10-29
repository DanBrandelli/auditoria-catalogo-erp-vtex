# Auditoria de qualidade de catálogo: ERP × VTEX

Ferramenta em **SQL + Python** que cruza o cadastro de produtos de um ERP (WK Radar) com o catálogo de uma loja VTEX e aponta inconsistências que causam erro de preço, frete, fiscal e busca no e-commerce.

> Os dados deste repositório são **fictícios**. A estrutura das planilhas reproduz o layout real, mas nenhum dado de empresa foi publicado.

## Problema

Quando o cadastro é manual e existem dois sistemas, o mesmo produto pode ter código de barras, NCM, peso, dimensões, status ou kit diferentes em cada lado. Em um catálogo de 800+ SKUs, essas divergências são difíceis de achar à mão e geram retrabalho e erros na loja.

## O que a auditoria verifica

| Consulta (`sql/`) | Pergunta de negócio |
|---|---|
| `01_so_no_erp` / `02_so_na_vtex` | Que produtos existem em apenas um dos sistemas? |
| `03_div_gtin_ean`, `04_div_ncm` | Código de barras e NCM batem? |
| `05_div_peso`, `06_div_dimensoes` | Peso e medidas divergem além da tolerância? |
| `07_div_status` | O status ativo/inativo é coerente? |
| `08_div_kit`, `09_kits_erp` | Kits do ERP estão marcados como kit na loja? Quantos componentes e peças cada um tem? |
| `10_qualidade_vtex` | Quantos SKUs ativos estão sem marca, meta descrição, EAN etc.? |
| `11_ean_duplicado`, `12_refid_multiplos_sku` | Há EAN repetido ou código com vários SKUs? |
| `13` a `15` (marcas) | Distribuição de marcas, grafias duplicadas e conteúdo do campo de marca do ERP |

Cada consulta está comentada com a pergunta que responde.

## Como funciona

1. O Python lê as duas planilhas e faz a limpeza (GTIN só com dígitos, números em formato BR, Sim/Não em booleano, uma linha por produto no ERP).
2. As tabelas `erp` e `vtex` ficam disponíveis para o DuckDB, que executa cada arquivo de `sql/`.
3. O resultado vira um Excel com uma aba de **resumo com percentuais** e uma aba por tipo de problema.

## Como rodar

```bash
pip install -r requirements.txt

# com os dados de exemplo
python auditoria_catalogo.py

# com as suas planilhas
python auditoria_catalogo.py --erp radar.xlsx --vtex vtex.xlsx --fator-peso-erp 1000
```

Opções: `--tolerancia 0.02` (diferença relativa aceita em peso e dimensões) e `--saida arquivo.xlsx`.

`python gerar_dados_exemplo.py` recria as planilhas fictícias.

## Decisões e limitações

- **Chave de cruzamento:** código do ERP = código de referência do produto na VTEX.
- **Marca:** o ERP tem uma marca única vinculada, então a marca comercial é auditada só na VTEX (completude e grafias duplicadas).
- **Peso:** a unidade pode diferir entre sistemas (kg × g). O script imprime uma razão mediana para ajudar a conferir e aceita `--fator-peso-erp`.
- **Kits:** assume que o ERP traz uma linha por componente de kit.
- Os dados reais devem ficar fora do repositório (`.gitignore` já bloqueia planilhas).

## Resultado

> Preencha com os números reais ao rodar na empresa (sem publicar dados), por exemplo: "X% dos SKUs com divergência de cadastro, Y marcas duplicadas, Z kits sem marcação na loja".

## Tecnologias

Python (pandas), SQL (DuckDB), Excel (openpyxl).

## Documentação

- 📘 [Manual de interpretação do relatório (PT-BR)](docs/MANUAL.md)
- 🌐 [Quick guide to reading the report (EN)](docs/MANUAL_EN.md)
