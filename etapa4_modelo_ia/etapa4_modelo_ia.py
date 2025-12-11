import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =========================================================
# 1. Carregar base gold
# =========================================================
df = pd.read_csv("gold_vendas.csv", low_memory=False)

# Garantir tipos
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df = df.dropna(subset=["CustomerID"])

# =========================================================
# 2. Criar base agregada por cliente
# =========================================================
agg = df.groupby("CustomerID").agg(
    total_compras=("InvoiceNo", "nunique"),
    total_gasto=("Receita", "sum"),
    ticket_medio=("Receita", "mean"),
    primeira_compra=("InvoiceDate", "min"),
    ultima_compra=("InvoiceDate", "max")
).reset_index()

# Calcular recência e frequência
agg["dias_entre_compras"] = (
    (agg["ultima_compra"] - agg["primeira_compra"]).dt.days /
    agg["total_compras"].replace(1, np.nan)
).fillna(0)

features = agg[["total_compras", "total_gasto", "ticket_medio", "dias_entre_compras"]]

# =========================================================
# 3. Normalizar os dados
# =========================================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# =========================================================
# 4. Aplicar K-Means (3 clusters)
# =========================================================
kmeans = KMeans(n_clusters=3, random_state=42)
agg["cluster"] = kmeans.fit_predict(X_scaled)

# =========================================================
# 5. Salvar resultado
# =========================================================
output_path = "clientes_clusterizados.csv"
agg.to_csv(output_path, index=False)

print("============================================")
print("MODELO DE AGRUPAMENTO (K-MEANS) EXECUTADO")
print(f"Clusters criados: {agg['cluster'].nunique()}")
print(f"Arquivo salvo: {output_path}")
print("============================================")
