import pandas as pd
import numpy as np

# ======================================
# 1. CARREGAR DADOS ORIGINAIS
# ======================================
CAMINHO_ARQUIVO = "Online Retail.xlsx"

df_raw = pd.read_excel(CAMINHO_ARQUIVO)

# Garantir tipos básicos
df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'], errors='coerce')

# ======================================
# 2. RELATÓRIO DE QUALIDADE DE DADOS
# ======================================
total_registros = len(df_raw)
total_colunas = len(df_raw.columns)

duplicados = df_raw.duplicated().sum()
nulos_total = df_raw.isna().sum().sum()
nulos_por_coluna = df_raw.isna().sum()

negativos_quantidade = (df_raw['Quantity'] < 0).sum()
preco_zero_negativo = (df_raw['UnitPrice'] <= 0).sum()
datas_invalidas = df_raw['InvoiceDate'].isna().sum()
clientes_sem_id = df_raw['CustomerID'].isna().sum()

print("\n==== RELATÓRIO DE QUALIDADE DE DADOS ====\n")
print(f"Total de registros: {total_registros}")
print(f"Total de colunas: {total_colunas}\n")

print("| Métrica                           | Valor |")
print("|----------------------------------|-------|")
print(f"| Linhas duplicadas                | {duplicados} |")
print(f"| Valores nulos (total)            | {nulos_total} |")
print(f"| Datas inválidas (InvoiceDate)    | {datas_invalidas} |")
print(f"| Quantidade negativa (Quantity)   | {negativos_quantidade} |")
print(f"| Preço zero ou negativo           | {preco_zero_negativo} |")
print(f"| Clientes sem ID (CustomerID)     | {clientes_sem_id} |")

print("\nDetalhamento de nulos por coluna:")
print(nulos_por_coluna)

# ======================================
# 3. CRIAR BASE LIMPA PARA ANÁLISES
#    (sem quebrar demais a base)
# ======================================

# Remover duplicados
df = df_raw.drop_duplicates().copy()

# Para métricas de venda, vamos considerar somente
# registros com data, quantidade e preço válidos
df_vendas = df.dropna(subset=['InvoiceDate', 'Quantity', 'UnitPrice']).copy()

# Filtrar quantidades e preços positivos para evitar distorções
df_vendas = df_vendas[(df_vendas['Quantity'] > 0) & (df_vendas['UnitPrice'] > 0)].copy()

# ======================================
# 4. ANÁLISES SOLICITADAS
# ======================================

print("\n\n==== ANÁLISES SOLICITADAS ====\n")

# ------------------------------
# 4.1 Top 5 produtos mais vendidos (por quantidade)
# ------------------------------
top5_produtos = (
    df_vendas
    .groupby('Description', as_index=False)['Quantity']
    .sum()
    .sort_values('Quantity', ascending=False)
    .head(5)
)

print("\nTop 5 produtos mais vendidos (por quantidade):")
print(top5_produtos)

# ------------------------------
# 4.2 Receita total por mês
# ------------------------------
df_vendas['Receita'] = df_vendas['Quantity'] * df_vendas['UnitPrice']
df_vendas['AnoMes'] = df_vendas['InvoiceDate'].dt.to_period('M').astype(str)

receita_por_mes = (
    df_vendas
    .groupby('AnoMes', as_index=False)['Receita']
    .sum()
    .sort_values('AnoMes')
)

print("\nReceita total por mês:")
print(receita_por_mes)

# ------------------------------
# 4.3 Taxa de retorno (clientes com 2+ pedidos)
# ------------------------------

# Usar somente registros com CustomerID válido
df_clientes = df_vendas.dropna(subset=['CustomerID']).copy()

compras_por_cliente = (
    df_clientes
    .groupby('CustomerID')['InvoiceNo']
    .nunique()
)

total_clientes = compras_por_cliente.count()
clientes_retorno = (compras_por_cliente > 1).sum()

taxa_retorno = clientes_retorno / total_clientes if total_clientes > 0 else np.nan

print("\nTaxa de retorno (clientes que compraram mais de uma vez):")
print(f"Total de clientes considerados: {total_clientes}")
print(f"Clientes com 2+ compras: {clientes_retorno}")
print(f"Taxa de retorno: {taxa_retorno:.2%}" if pd.notnull(taxa_retorno) else "Taxa de retorno: não calculada")

# ------------------------------
# 4.4 Média de tempo entre compras por cliente
# ------------------------------

df_clientes = df_clientes.sort_values(['CustomerID', 'InvoiceDate']).copy()
df_clientes['DiffDias'] = df_clientes.groupby('CustomerID')['InvoiceDate'].diff().dt.days

# Ignorar a primeira compra (diff = NaN)
intervalos_validos = df_clientes.dropna(subset=['DiffDias']).copy()

media_por_cliente = (
    intervalos_validos
    .groupby('CustomerID')['DiffDias']
    .mean()
)

media_geral_dias = media_por_cliente.mean()

print("\nMédia de tempo entre compras por cliente:")
print(f"Clientes considerados: {media_por_cliente.shape[0]}")
print(f"Média geral de dias entre compras: {media_geral_dias:.2f} dias" if not np.isnan(media_geral_dias) else "Não foi possível calcular a média de dias entre compras.")
