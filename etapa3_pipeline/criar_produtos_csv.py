import pandas as pd

# =========================================================
# GERAÇÃO DO ARQUIVO produtos.csv A PARTIR DA GOLD
# =========================================================

def gerar_produtos():
    df = pd.read_csv("gold_vendas.csv")

    produtos = (
        df[['StockCode', 'Description', 'UnitPrice']]
        .drop_duplicates()
        .rename(columns={'StockCode': 'ProductID'})
    )

    produtos.to_csv("produtos.csv", index=False)
    print("Arquivo 'produtos.csv' criado com sucesso.")

if __name__ == "__main__":
    gerar_produtos()
