# PROJETO — Análise de Vendas, Enriquecimento de Produto com TF-IDF, Pipeline Automatizado e Clusterização de Clientes  
## Estrategista de Dados e Negócios

Projeto dividido em quatro etapas, evoluindo da exploração de dados, passando por engenharia semântica, automação e modelagem de Machine Learning.

---

## ETAPA 1 — Diagnóstico, Limpeza e Exploração da Base Online Retail

**Objetivo:** compreender a integridade dos dados, comportamento de compra e calcular KPIs essenciais.

### Entregas

| Arquivo | Descrição |
|--------|-----------|
| **ETAPA_1_DIAGNOSTICO_DADOS.md** | Levantamento de nulos, duplicados, inconsistências e impacto no negócio |
| **etapa1_analise.py** | Script Python contendo diagnóstico, tratamento e análises |
| **etapa1_kpis.sql** | Respostas às perguntas de negócio via SQL |
| **KPIs Respondidos** | Top 5 produtos, receita mensal, taxa de retorno, intervalo médio de recompra |

### Critérios de Tratamento Aplicados

- CustomerID nulo: incluído na visão geral e excluído das análises comportamentais  
- Preços zerados ou negativos: removidos  
- Datas inválidas: excluídas  
- Duplicidades: eliminadas  
- A base apresenta aproximadamente **25% de registros sem CustomerID**, portanto análises paralelas foram feitas para avaliar impacto.

### Insights de Negócio (Etapa 1)

- **Taxa de retorno acima de 65%** → forte comportamento de recompra e oportunidade de fidelização  
- **Recompra média em ~3 dias** → consumo recorrente ou complementar  
- A exclusão de registros sem CustomerID **não altera significativamente os KPIs**, reforçando consistência nos dados identificados  

---

## ETAPA 2 — Enriquecimento Semântico e Taxonomia de Produto (TF-IDF + KMeans)

### Problema
A base original não contém categoria de produto, impossibilitando análises essenciais:

- Receita por categoria  
- Mix de portfólio  
- Curva ABC  
- Retenção por tipo de produto  

### Solução
Aplicação de:

- **TF-IDF** para vetorização de descrições de produto  
- **KMeans** para clusterização por similaridade semântica  
- Construção de **3 níveis hierárquicos**

### Estrutura da Taxonomia Criada

| Nível | Descrição |
|-------|-----------|
| **CategoriaN1** | Macro Categoria |
| **CategoriaN2** | Categoria |
| **CategoriaN3** | Subcategoria |

Essa hierarquia permite drill-down no Power BI e visão analítica estruturada.

### Arquivos da Etapa 2

| Arquivo | Função |
|---------|--------|
| **categorizar_produtos.py** | Clusterização TF-IDF + KMeans |
| **adicionar_taxonomia.py** | Geração das categorias N1, N2 e N3 |
| **produtos_categorizados_taxonomia.csv** | Dataset enriquecido |
| **dashboard_data_teste.pbix** | Dashboard Power BI |
| **print_dashboard_data_teste.png** | Versão estática do dashboard |

### Visualizações Criadas no Dashboard Power BI

- Receita por Macro Categoria  
- Receita por Categoria e Subcategoria  
- Drill-down completo do produto  
- Comparação de desempenho entre categorias  

### Tecnologias Utilizadas

- Python (Pandas, Scikit-Learn)  
- Power BI  
- SQLite  
- GitHub  

---

## ETAPA 3 — Pipeline Automatizado (Simulação de Envio de E-mail)

**Arquivo principal:** `etapa3_pipeline.py`

### Fluxo Implementado

1. Leitura dos arquivos `produtos.csv` e `vendas.csv`  
2. Junção das tabelas pela coluna `ProductID`  
3. Geração automática do relatório diário `relatorio_diario_YYYY-MM-DD.csv` contendo:
   - Total_Vendas  
   - Qtde_Transacoes  
   - Qtde_Clientes  
4. Simulação de envio de e-mail:
   - Exibição no console do destinatário, título e arquivo enviado  

### Execução

```bash
python etapa3_pipeline.py

---

## ETAPA 4 — Modelo de IA (Clusterização de Clientes)

**Objetivo:** aplicar técnicas de aprendizado não supervisionado para identificar perfis distintos de clientes com base no comportamento de compra registrado na base `gold_vendas.csv`.

A etapa complementa o ciclo analítico iniciado nas fases anteriores, permitindo extrair inteligência aplicada para segmentação, marketing e decisões de negócio.

---

### Abordagem Adotada

Foi utilizado o algoritmo **K-Means**, pela combinação de:

- simplicidade e eficiência;
- boa performance com poucas features numéricas;
- fácil interpretabilidade dos resultados;
- ausência de necessidade de variável-alvo (aprendizado não supervisionado).

A preparação dos dados incluiu:

- agregação das vendas por `CustomerID`;  
- cálculo de métricas comportamentais;  
- normalização com **StandardScaler** para evitar distorção de variáveis em escalas diferentes;  
- definição de **3 clusters** como ponto de equilíbrio entre explicabilidade e separação dos grupos.

---

### Arquivo Principal

| Arquivo | Função |
|---------|--------|
| **etapa4_modelo_ia.py** | Executa toda a lógica de agregação, normalização, clusterização e exportação dos resultados |

---

### Funcionalidades Implementadas

O script realiza as seguintes operações:

1. **Leitura da base `gold_vendas.csv`**
   - A base consolidada (gold layer) contém registros transacionais já tratados.

2. **Agregação por cliente**
   - Métricas calculadas:
     - `total_compras` — número de faturas distintas  
     - `total_gasto` — valor total consumido  
     - `ticket_medio` — gasto médio por transação  
     - `primeira_compra` — data mínima  
     - `ultima_compra` — data máxima  
     - `dias_entre_compras` — frequência estimada  

3. **Normalização das variáveis numéricas**
   - Evita que métricas com magnitude maior dominem o algoritmo.

4. **Treinamento do K-Means**
   - Número de clusters definido como **3**.
   - Atribuição do cluster a cada cliente.

5. **Exportação do arquivo enriquecido**
   - Gera `clientes_clusterizados.csv` contendo:
     - CustomerID  
     - Métricas agregadas  
     - Cluster atribuído  

---

### Fórmulas e Detalhes Técnicos

**Frequência média de recompra:**

\[
dias\_entre\_compras = \frac{ultima\_compra - primeira\_compra}{total\_compras}
\]

**Variáveis normalizadas com StandardScaler:**

- `total_compras`  
- `total_gasto`  
- `ticket_medio`  
- `dias_entre_compras`

---

### Execução

Para rodar o modelo:

```bash
python etapa4_modelo_ia.py
