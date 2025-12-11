import pandas as pd
from datetime import datetime

# =========================================================
# ETAPA 3 - Pipeline Automatizado de Vendas (ENVIO SIMULADO)
# =========================================================

def carregar_dados():
    """Lê os arquivos de produtos e vendas gerados a partir da base GOLD."""
    produtos = pd.read_csv("produtos.csv")
    vendas = pd.read_csv("vendas.csv")
    return produtos, vendas


def gerar_relatorio_diario(produtos: pd.DataFrame, vendas: pd.DataFrame) -> str:
    """Une as bases e gera um relatório diário agregado em CSV."""

    # merge pela coluna ProductID
    base = vendas.merge(produtos, on="ProductID", how="left")

    # garantir formatação da data
    base["InvoiceDate"] = pd.to_datetime(base["InvoiceDate"])
    base["Data"] = base["InvoiceDate"].dt.date

    # relatório diário agregado
    relatorio = (
        base.groupby("Data", as_index=False)
            .agg(
                Total_Vendas=("TotalPrice", "sum"),
                Qtde_Transacoes=("InvoiceNo", "nunique"),
                Qtde_Clientes=("CustomerID", "nunique")
            )
    )

    # nome do arquivo de saída
    nome_arquivo = f"relatorio_diario_{datetime.today().date()}.csv"
    relatorio.to_csv(nome_arquivo, index=False)

    return nome_arquivo


def enviar_email_simulado(caminho_arquivo: str) -> None:
    """
    Simula o envio de e-mail com o relatório diário.
    Este comportamento atende exatamente ao escopo do teste.
    """
    print("====================================================")
    print("SIMULAÇÃO DE ENVIO DE E-MAIL - PIPELINE AUTOMATIZADO")
    print(f"Relatório diário gerado: {caminho_arquivo}")
    print("Destinatário: jgslessa@gmail.com")
    print("Assunto: Relatório diário de vendas")
    print("Anexo: arquivo CSV agregado por dia")
    print("Status: ENVIADO (simulado)")
    print("====================================================")


if __name__ == "__main__":
    produtos_df, vendas_df = carregar_dados()
    caminho_rel = gerar_relatorio_diario(produtos_df, vendas_df)
    enviar_email_simulado(caminho_rel)
