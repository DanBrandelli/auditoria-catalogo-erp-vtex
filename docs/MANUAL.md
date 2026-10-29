# Manual: como ler o relatório de auditoria do catálogo (ERP × Loja)

*Guia prático para quem não é de TI: entender, comparar e corrigir divergências de cadastro.*

> Este manual acompanha o projeto de auditoria de catálogo (SQL + Python). Os exemplos usam **dados fictícios**. [Read the short English version](MANUAL_EN.md).

## 1. Para que serve

Empresas de e-commerce costumam ter **dois cadastros de produtos**: o do **ERP** (sistema interno) e o da **loja virtual** (o que o cliente vê). Quando eles não dizem a mesma coisa, surgem erros de frete, de nota fiscal, de busca e de estoque.

O script compara os dois cadastros e gera um Excel (`relatorio.xlsx`) com **uma aba para cada tipo de problema**. Este manual ensina a ler cada aba e a decidir o que corrigir.

| Sistema | O que é | Colunas no relatório |
|---|---|---|
| 🏭 **ERP** | cadastro interno: fiscal, peso, medidas, kits | sufixo `_erp` |
| 🛒 **Loja** | vitrine: nome, marca, descrição, EAN, medidas de envio | sufixo `_vtex` |

## 2. As 4 regras de ouro

> **1. Divergência não é sempre erro.** O relatório mostra onde há diferença. Quem decide se é erro é a pessoa, olhando o produto.
>
> **2. Confira antes de corrigir.** Abra o produto nos dois sistemas.
>
> **3. Defina qual sistema manda em cada campo** (seção 6).
>
> **4. Não corrija em massa sem validar.** Dados fiscais e de preço devem passar pelo responsável da área.

## 3. O mapa do relatório

Legenda de gravidade: 🔴 crítico · 🟠 alto · 🟡 médio · 🔵 baixo (qualidade)

| Aba | Pergunta que responde | Gravidade |
|---|---|---|
| `resumo` | Qual o tamanho geral do problema? | 📊 visão geral |
| `so_na_vtex` | O que está à venda na loja mas não existe no ERP? | 🔴 |
| `div_status` | Algum item está inativo em um sistema e ativo no outro? | 🔴 |
| `so_no_erp` | O que existe no ERP mas não está na loja? | 🟠 |
| `div_ncm` | A classificação fiscal é a mesma? | 🟠 |
| `div_gtin_ean` | O código de barras é o mesmo? | 🟠 |
| `div_peso` | O peso é o mesmo? | 🟡 |
| `div_dimensoes` | Largura, altura e comprimento são os mesmos? | 🟡 |
| `div_kit` / `kits_erp` | Os kits estão marcados corretamente? | 🟡 |
| `qualidade_vtex` | Quantos produtos têm campos vazios? | 🔵 |
| `ean_duplicado` | O mesmo código de barras aparece em mais de um produto? | 🔵 |
| `marcas_vtex` / `marcas_grafia_parecida` | As marcas estão padronizadas? | 🔵 |
| `marca_comercial_erp` | O campo de marca do ERP serve de referência? | 🔵 |

### Comece pelo `resumo`

| Percentual | Significa | O que fazer |
|---|---|---|
| 🟢 até 5% | poucos casos | corrigir caso a caso |
| 🟡 de 5% a 30% | problema moderado | corrigir por lotes |
| 🔴 acima de 30% | problema grande **ou** erro de método | investigar a causa antes de corrigir |

⚠️ Se o indicador "Produtos ERP encontrados na VTEX" for baixo, o cruzamento não funcionou (códigos diferentes entre os sistemas). Resolva isso antes de corrigir qualquer coisa.

## 4. Como ler qualquer aba em 4 passos

1. **Veja o código.** A primeira coluna (`codigo` ou `refid`) identifica o produto.
2. **Compare os pares.** Colunas com `_erp` e `_vtex` mostram o mesmo dado nos dois sistemas.
3. **Pergunte: quem está certo?** Veja o produto físico, a nota fiscal ou a embalagem.
4. **Anote e corrija** no sistema errado, registrando em uma planilha de acompanhamento (seção 7).

**Exemplo (aba `div_gtin_ean`):**

| codigo | nome | gtin_erp | ean_vtex |
|---|---|---|---|
| P004 | Microscópio digital | 7890000000042 | 7890000009999 |

👉 O mesmo produto tem dois códigos de barras. Se a embalagem mostra `...0042`, o erro está na loja e deve ser corrigido lá.

## 5. Guia aba por aba

### 🔴 `so_na_vtex`: à venda, mas sem cadastro no ERP
- **Causas comuns:** código digitado diferente (espaço, zero à esquerda), produto criado só na loja, item que mudou de código.
- **O que fazer:** procure o produto no ERP pelo nome ou EAN. Se existe com outro código, corrija o código. Se não existe, cadastre no ERP ou desative na loja.

### 🔴 `div_status`: ativo em um lado, inativo no outro

| status_erp | status_vtex | Situação | Ação |
|---|---|---|---|
| inativo | **ativo** | 🔴 vendendo item descontinuado | desativar na loja (ou reativar no ERP, se foi engano) |
| ativo | inativo | 🟡 item some da loja sem motivo | reativar na loja, se deve ser vendido |

### 🟠 `so_no_erp`: no ERP, mas não está na loja
Nem todo item precisa estar na loja (insumos, itens de uso interno). Separe em dois grupos: **deveria estar à venda** (cadastrar na loja) e **não precisa** (sem ação).

### 🟠 `div_ncm`: classificação fiscal diferente
Pontos e traços já foram removidos, então a diferença é real. O NCM define impostos: confirme com a área fiscal qual é o correto antes de alterar.

### 🟠 `div_gtin_ean`: código de barras diferente

| Caso | Leitura | Ação |
|---|---|---|
| códigos diferentes | um dos dois está errado | conferir na embalagem |
| preenchido em um lado, vazio no outro | falta cadastrar | copiar o código correto |
| dois produtos com o mesmo código | veja `ean_duplicado` | conferir qual é o correto |

### 🟡 `div_peso`: peso diferente

| Observação | Leitura | Ação |
|---|---|---|
| **quase todos** os produtos aparecem | unidade diferente (kg × g) | não é erro de cadastro; rode o script com o ajuste de unidade |
| poucos produtos aparecem | divergência real | pesar com a embalagem e corrigir |

💡 ERP com `1,2` (kg) e loja com `1200` (g) é o **mesmo peso**.

### 🟡 `div_dimensoes`: medidas diferentes
O ERP pode guardar a medida do **produto** e a loja a da **embalagem**: isso é diferença de conceito, não erro. Para frete, vale a medida da embalagem. Meça na prática os casos duvidosos.

### 🟡 `div_kit` e `kits_erp`: kits

| kit_no_erp | kit_na_vtex | Leitura | Ação |
|---|---|---|---|
| ✔️ sim | ✖️ não | é kit no ERP, mas a loja trata como produto simples | marcar como kit na loja |
| ✖️ não | ✔️ sim | a loja diz que é kit, o ERP não | conferir qual está certo |

Na aba `kits_erp`, **n_componentes** é quantos itens *diferentes* o kit tem e **total_pecas** é a soma das quantidades. Exemplo: 1 câmera + 2 cartões = `n_componentes 2`, `total_pecas 3`.

### 🔵 `qualidade_vtex`: campos vazios
É uma linha só. Para o percentual, divida cada coluna por `total_sku`.

| Coluna | Impacto de estar vazio |
|---|---|
| `sem_marca` | quebra filtros e busca por marca |
| `sem_meta_descricao` | pior aparência no Google |
| `sem_titulo_pagina` | pior posicionamento no Google |
| `sem_descricao` | cliente sem informação |
| `sem_ean` | problemas em integrações e marketplaces |
| `sem_departamento` | produto sem categoria na loja |

### 🔵 `ean_duplicado`
Mostra o mesmo código de barras em mais de um produto. Pode ser erro de digitação ou cadastro duplicado. Kit e produto individual às vezes compartilham o EAN de propósito: confira antes de concluir.

### 🔵 `marcas_vtex` e `marcas_grafia_parecida`
A linha em branco de `marcas_vtex` são os produtos sem marca. A aba `marcas_grafia_parecida` lista marcas escritas de formas diferentes que são a mesma:

| grafias | Problema | Ação |
|---|---|---|
| Intelbras \| INTELBRAS \| Intelbrás | o filtro da loja mostra 3 marcas | escolher **uma** grafia oficial e padronizar |

### 🔵 `marca_comercial_erp`
Se aparecer um valor só, o campo não serve de referência: a marca correta existe apenas na loja.

## 6. Quem manda em cada campo (exemplo de política)

Sugestão inicial. **Cada organização deve definir e registrar a sua.**

| Dado | Sistema que deve mandar | Por quê |
|---|---|---|
| NCM | 🏭 ERP, validado pela área fiscal | impacto em impostos |
| Código de barras | 📦 embalagem do produto | fonte física |
| Peso e medidas | 📏 medição real da embalagem | usado no frete |
| Status ativo/inativo | 🏭 ERP | controla compra e estoque |
| Composição de kit | 🏭 ERP | tem a lista de componentes |
| Marca, descrição, título, meta | 🛒 Loja | conteúdo de vitrine |

## 7. Roteiro de correção em 5 etapas

| Etapa | O que fazer | Abas |
|---|---|---|
| **1** 🔴 | Parar de vender o que não existe ou está descontinuado | `div_status`, `so_na_vtex` |
| **2** 🟠 | Acertar fiscal e códigos de barras | `div_ncm`, `div_gtin_ean`, `so_no_erp` |
| **3** 🟡 | Corrigir peso, medidas e kits | `div_peso`, `div_dimensoes`, `div_kit` |
| **4** 🔵 | Preencher campos vazios | `qualidade_vtex` |
| **5** 🔵 | Padronizar marcas e tratar EAN duplicado | `marcas_grafia_parecida`, `ean_duplicado` |

**Planilha de acompanhamento (colunas sugeridas):**

| código | aba de origem | problema | valor ERP | valor loja | quem está certo | onde corrigir | responsável | status | data |
|---|---|---|---|---|---|---|---|---|---|
| P004 | div_gtin_ean | EAN diferente | ...0042 | ...9999 | ERP (conferido na embalagem) | Loja | — | ✅ feito | — |

Status sugeridos: ⬜ a fazer · 🟨 em andamento · ✅ feito · ⏸️ aguardando decisão.

## 8. Armadilhas comuns

| ⚠️ Armadilha | Como evitar |
|---|---|
| Peso 100% diferente | é unidade (kg × g); ajuste antes de interpretar |
| Código "igual" que não bate | espaço sobrando ou zero à esquerda |
| Um produto aparece repetido | ele tem mais de um SKU (variação) |
| Muitos itens "só no ERP" | podem ser itens que nunca iriam para a loja |
| Kit com números estranhos | confirme com um kit conhecido qual coluna é o kit e qual é o componente |
| Corrigir sem conferir | olhe sempre o produto físico ou o documento antes |

## 9. Checklist final

- ⬜ Li o `resumo` e o percentual de produtos conciliados está razoável
- ⬜ Conferi 3 a 5 casos de cada aba nas planilhas originais
- ⬜ Defini quem manda em cada campo
- ⬜ Criei a planilha de acompanhamento
- ⬜ Corrigi na ordem de prioridade
- ⬜ Rodei o script de novo e comparei os percentuais antes e depois

💡 Guarde o `resumo` de **antes** e de **depois**: a diferença é o resultado do trabalho.

## 10. Glossário

| Termo | Significa |
|---|---|
| **ERP** | sistema interno de gestão |
| **SKU** | cada versão vendável de um produto (cor, tamanho etc.) |
| **GTIN / EAN** | número do código de barras |
| **NCM** | classificação fiscal do produto |
| **Kit** | produto formado por outros produtos |
| **Conciliar** | comparar os dois sistemas e ver se dizem o mesmo |
| **Divergência** | diferença entre os dois sistemas (nem sempre é erro) |
| **Fonte da verdade** | sistema ou documento que vale quando há conflito |
