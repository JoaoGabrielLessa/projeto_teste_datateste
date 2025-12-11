import pandas as pd

# =========================================================
# GERAÇÃO DO ARQUIVO vendas.csv A PARTIR DA GOLD
# =========================================================

def gerar_vendas():
    df = pd.read_csv("gold_vendas.csv")

    vendas = (
        df[['InvoiceNo', 'StockCode', 'CustomerID', 'InvoiceDate',
             'Quantity', 'UnitPrice', 'Receita']]
        .rename(columns={
            'StockCode': 'ProductID',
            'Receita': 'TotalPrice'
        })
    )

    vendas.to_csv("vendas.csv", index=False)
    print("Arquivo 'vendas.csv' criado com sucesso.")

if __name__ == "__main__":
    gerar_vendas()
