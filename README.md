PROJETO — Análise de Vendas, Enriquecimento de Produto com TF-IDF, Pipeline Automatizado e Clusterização de Clientes
Estrategista de Dados e Negócios

Projeto dividido em quatro etapas, evoluindo da exploração de dados, passando por engenharia semântica, automação e modelagem de Machine Learning.

ETAPA 1 — Diagnóstico, Limpeza e Exploração da Base Online Retail

Objetivo: compreender a integridade dos dados, comportamento de compra e calcular KPIs essenciais.

Entregas
Arquivo	Descrição
ETAPA_1_DIAGNOSTICO_DADOS.md	Levantamento de nulos, duplicados, inconsistências e impacto no negócio
etapa1_analise.py	Script Python contendo diagnóstico, tratamento e análises numéricas
etapa1_kpis.sql	Respostas às perguntas de negócio via SQL
KPIs Respondidos	Top 5 produtos, receita mensal, taxa de retorno, intervalo médio de recompra
Critérios de Tratamento Aplicados

CustomerID nulo: incluído na visão geral e excluído de análises comportamentais

Preços zerados/negativos: removidos

Datas inválidas: excluídas

Duplicidades: eliminadas

Aproximadamente 25% da base sem CustomerID — análises foram realizadas em paralelo para avaliar impacto.
