# PROJETO — Análise de Vendas, Enriquecimento de Produto com TF-IDF, Pipeline Automatizado e Clusterização de Clientes  
## Estrategista de Dados e Negócios

Projeto dividido em quatro etapas, evoluindo da exploração de dados, passando por engenharia semântica, automação e modelagem de Machine Learning.

---

## ETAPA 1 — Diagnóstico, Limpeza e Exploração da Base Online Retail

Objetivo: compreender a integridade dos dados, comportamento de compra e calcular KPIs essenciais.

### Entregas

| Arquivo | Descrição |
|--------|-----------|
| ETAPA_1_DIAGNOSTICO_DADOS.md | Levantamento de nulos, duplicados, inconsistências e impacto no negócio |
| etapa1_analise.py | Script Python contendo diagnóstico, tratamento e análises |
| etapa1_kpis.sql | Respostas às perguntas de negócio via SQL |
| KPIs Respondidos | Top 5 produtos, receita mensal, taxa de retorno, intervalo médio de recompra |

### Critérios de Tratamento Aplicados

- CustomerID nulo: incluído na visão geral e excluído das análises comportamentais  
- Preços zerados ou negativos: removidos  
- Datas inválidas: excluídas  
- Duplicidades: eliminadas  
- A base apresenta aproximadamente 25% de registros sem CustomerID; análises comparativas foram realizadas para avaliar impacto.

### Insights de Negócio (Etapa 1)

- Taxa de retorno acima de 65% indica forte comportamento de recompra  
- Recompra média em aproximadamente 3 dias sugere consumo recorrente ou complementar  
- Exclusão de registros sem CustomerID não altera significativamente os KPIs, reforçando consistência dos dados identificados  

---

## ETAPA 2 — Enriquecimento Semântico e Taxonomia de Produto (TF-IDF + KMeans)

### Problema

A base original não contém categoria de produto, impossibilitando análises gerenciais como:

- Receita por categoria  
- Mix de portfólio  
- Curva ABC  
- Retenção por tipo de produto  

### Solução Aplicada

- Vetorização das descrições via TF-IDF  
- Agrupamento semântico por similaridade utilizando KMeans  
- Criação de três níveis hierárquicos de categoria

### Estrutura da Taxonomia Criada

| Nível | Descrição |
|-------|-----------|
| CategoriaN1 | Macro Categoria |
| CategoriaN2 | Categoria |
| CategoriaN3 | Subcategoria |

### Arquivos da Etapa 2

| Arquivo | Função |
|---------|--------|
| categorizar_produtos.py | Geração dos clusters via TF-IDF + KMeans |
| adicionar_taxonomia.py | Construção dos níveis de categoria |
| produtos_categorizados_taxonomia.csv | Dataset enriquecido |
| dashboard_data_teste.pbix | Dashboard Power BI |
| print_dashboard_data_teste.png | Visualização estática do dashboard |

### Visualizações Criadas no Dashboard Power BI

- Receita por Macro Categoria  
- Receita por Categoria e Subcategoria  
- Drill-down completo de produto  
- Comparação de desempenho entre categorias  

### Tecnologias Utilizadas

- Python (Pandas, Scikit-Learn)  
- Power BI  
- SQLite  
- GitHub  

---

## ETAPA 3 — Pipeline Automatizado (Simulação de Envio de E-mail)

Arquivo principal: etapa3_pipeline.py

### Fluxo Implementado

1. Leitura dos arquivos produtos.csv e vendas.csv  
2. Junção das tabelas pela coluna ProductID  
3. Geração automática do relatório diário relatorio_diario_YYYY-MM-DD.csv contendo:  
   - Total_Vendas  
   - Qtde_Transacoes  
   - Qtde_Clientes  
4. Simulação de envio de e-mail com exibição no console do destinatário, título e arquivo enviado  

### Execução

```bash
python etapa3_pipeline.py

```markdown
## ETAPA 4 — Modelo de IA (Agrupamento de Clientes)

Objetivo: aplicar Machine Learning não supervisionado para identificar perfis de clientes com base no comportamento de compra registrado na base `gold_vendas.csv`.

### Entregas

| Arquivo | Descrição |
|---------|-----------|
| etapa4_modelo_ia.py | Script que lê a base, agrega métricas por cliente, normaliza variáveis e aplica K-Means |
| clientes_clusterizados.csv | Dataset final contendo métricas agregadas e o cluster atribuído a cada cliente |

### Abordagem Adotada

Foi utilizada uma técnica de aprendizado não supervisionado (K-Means), adequada quando não há variável-alvo definida e deseja-se identificar grupos com padrões semelhantes.

Os principais passos incluem:

- Agregação das compras por CustomerID  
- Cálculo das métricas de comportamento  
- Normalização das variáveis numéricas  
- Treinamento do modelo K-Means com 3 clusters  
- Interpretação dos grupos sob a ótica de negócio  

### Features Utilizadas por Cliente

As métricas derivadas da base incluem:

- total_compras — quantidade de faturas distintas  
- total_gasto — soma total da coluna Receita  
- ticket_medio — média de gasto por compra  
- primeira_compra — data da primeira compra  
- ultima_compra — data da última compra  
- dias_entre_compras — estimado por:  

\[
dias\_entre\_compras = \frac{ultima\_compra - primeira\_compra}{total\_compras}
\]

As variáveis numéricas foram padronizadas com StandardScaler.

### Execução

```bash
python etapa4_modelo_ia.py
