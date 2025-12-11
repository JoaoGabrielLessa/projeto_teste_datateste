import pandas as pd

# =========================================================
# Arquivo de entrada (o mesmo que você já carregou no BI)
# =========================================================
df = pd.read_csv("produtos_categorizados.csv")

# =========================================================
# Dicionário de taxonomia 3 níveis
# =========================================================
cluster_name_map = {
    0: ("Gifts & Packaging","Gift Boxes","Vintage Small Box"),
    1: ("Home Decor","Romantic Decor","Hanging Heart"),
    2: ("Home Decor","Floral & Craft Decor","Pink Polkadot Floral"),
    3: ("Home Decor","Candle Holders","Hanging Glass Holder"),
    4: ("Home Decor","Wall Signs","Vintage French Metal Sign"),
    5: ("Party & Events","Party Sets","Vintage Cards & Lights"),
    6: ("Seasonal","Christmas","Jumbo Gift Bags & Tree"),
    7: ("Home Decor","Wall Decor","Vintage Glass Wall Design"),
    8: ("Jewelry & Accessories","Necklaces","Shell & Glass Pendant"),
    9: ("Jewelry & Accessories","Earrings","Drop Crystal Beads")
}

# =========================================================
# Aplicar ao dataframe
# =========================================================
df[['CategoriaN1','CategoriaN2','CategoriaN3']] = pd.DataFrame(
    df['Cluster'].map(cluster_name_map).tolist(),
    index=df.index
)

# =========================================================
# Salvar o novo CSV
# =========================================================
output = "produtos_categorizados_taxonomia.csv"
df.to_csv(output, index=False, encoding="utf-8-sig")

print(f"✔ Arquivo salvo com sucesso: {output}")
