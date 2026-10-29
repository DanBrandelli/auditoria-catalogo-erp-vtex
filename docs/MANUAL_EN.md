# Quick guide: reading the catalog audit report (ERP × Online Store)

*Short English version of the full manual in Portuguese: [MANUAL.md](MANUAL.md).*

## What this is

The audit script compares the product catalog of an **ERP** with the catalog of an **e-commerce platform (VTEX)** and produces an Excel report with **one sheet per type of data problem**. Examples use **fictional data**.

Key rule: **a mismatch is not always an error.** The report shows where to look. A person decides what is wrong by checking the product itself.

## 3. Report map

Severity: 🔴 critical · 🟠 high · 🟡 medium · 🔵 low (data quality)

| Sheet | Question it answers | Severity |
|---|---|---|
| `resumo` | How big is the problem overall? | 📊 overview |
| `so_na_vtex` | What is on sale in the store but missing in the ERP? | 🔴 |
| `div_status` | Is any item inactive in one system and active in the other? | 🔴 |
| `so_no_erp` | What exists in the ERP but is not in the store? | 🟠 |
| `div_ncm` | Is the tax classification (NCM) the same? | 🟠 |
| `div_gtin_ean` | Is the barcode the same? | 🟠 |
| `div_peso` | Is the weight the same? | 🟡 |
| `div_dimensoes` | Are width, height and length the same? | 🟡 |
| `div_kit` / `kits_erp` | Are kits flagged correctly? How many components and pieces? | 🟡 |
| `qualidade_vtex` | How many active SKUs have empty key fields? | 🔵 |
| `ean_duplicado` | Is the same barcode used on more than one product? | 🔵 |
| `marcas_vtex` / `marcas_grafia_parecida` | Are brand names standardized? | 🔵 |
| `marca_comercial_erp` | Is the ERP brand field usable as a reference? | 🔵 |

Sheet and column names are in Portuguese because the source systems and the report are in Portuguese. Columns ending in `_erp` come from the ERP and `_vtex` from the online store.

### Start with the summary

| Percentage | Meaning | Action |
|---|---|---|
| 🟢 up to 5% | few cases | fix one by one |
| 🟡 5% to 30% | moderate | fix in batches |
| 🔴 above 30% | large problem **or** method error | investigate the cause first |

⚠️ If "ERP products found in VTEX" is low, the match between systems failed (different product codes). Fix that before correcting anything.

## 4. How to read any sheet in 4 steps

1. **Find the code.** The first column (`codigo` or `refid`) identifies the product.
2. **Compare the pairs.** `_erp` and `_vtex` columns show the same data in both systems.
3. **Ask who is right.** Check the physical product, invoice or packaging.
4. **Log and fix** it in the wrong system, tracking progress in a spreadsheet.

**Example (sheet `div_gtin_ean`):**

| codigo | nome | gtin_erp | ean_vtex |
|---|---|---|---|
| P004 | Digital microscope | 7890000000042 | 7890000009999 |

👉 The same product has two different barcodes. If the packaging shows `...0042`, the store record is wrong and should be fixed there.

## Common pitfalls

| ⚠️ Pitfall | How to avoid it |
|---|---|
| Weight differs in nearly 100% of products | unit mismatch (kg vs g); adjust the unit before interpreting |
| Codes look equal but do not match | trailing space or leading zero |
| A product appears more than once | it has several SKUs (variants) |
| Many items only in the ERP | they may never have been meant for the store |
| Odd kit numbers | confirm with a known kit which column is the parent and which is the component |

## Suggested fix order

1. 🔴 Status and items missing from the ERP (`div_status`, `so_na_vtex`)
2. 🟠 Tax and barcodes (`div_ncm`, `div_gtin_ean`, `so_no_erp`)
3. 🟡 Weight, dimensions and kits (`div_peso`, `div_dimensoes`, `div_kit`)
4. 🔵 Empty fields (`qualidade_vtex`)
5. 🔵 Brand names and duplicate barcodes (`marcas_grafia_parecida`, `ean_duplicado`)

💡 Keep the `resumo` sheet from **before** and **after** the fixes. The difference is the measurable result of the cleanup.
