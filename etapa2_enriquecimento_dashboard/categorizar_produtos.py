import re
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk import download
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# =========================================================
# 1. Configurações básicas
# =========================================================

INPUT_FILE = "produtos.csv"               # nome do arquivo de entrada
OUTPUT_FILE = "produtos_categorizados.csv"  # nome do arquivo de saída
K_CLUSTERS = 10                           # número inicial de clusters (ajustável)


# =========================================================
# 2. Baixar stopwords (apenas primeira vez)
# =========================================================

print("➡ Baixando stopwords (se necessário)...")
download('stopwords')


# =========================================================
# 3. Carregar dados
# =========================================================

print(f"➡ Lendo arquivo: {INPUT_FILE}")
df = pd.read_csv(INPUT_FILE, encoding="utf-8")

# Detectar coluna de descrição
if 'Description' in df.columns:
    df.rename(columns={'Description': 'text'}, inplace=True)
elif 'description' in df.columns:
    df.rename(columns={'description': 'text'}, inplace=True)
else:
    raise ValueError("❌ Não encontrei coluna 'Description' ou 'description' no CSV.")

print(f"✔ Total de linhas: {len(df)}")


# =========================================================
# 4. Limpeza de texto
# =========================================================

stop_words = set(stopwords.words('english'))  # stopwords em inglês, base original é inglesa


def limpar_texto(texto: str) -> str:
    texto = str(texto).lower()
    # remove tudo que não for letra ou espaço
    texto = re.sub(r'[^a-z\s]', ' ', texto)
    tokens = texto.split()
    # remove stopwords
    tokens = [t for t in tokens if t not in stop_words]
    return " ".join(tokens)


print("➡ Limpando textos...")
df['clean_text'] = df['text'].apply(limpar_texto)


# =========================================================
# 5. Vetorização TF-IDF
# =========================================================

print("➡ Gerando matriz TF-IDF...")
vectorizer = TfidfVectorizer(max_features=2000)
X = vectorizer.fit_transform(df['clean_text'])


# =========================================================
# 6. Clustering com KMeans
# =========================================================

print(f"➡ Rodando KMeans com k={K_CLUSTERS} clusters...")
kmeans = KMeans(n_clusters=K_CLUSTERS, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X)

terms = vectorizer.get_feature_names_out()

# Descobrir termos mais fortes de cada cluster
cluster_top_terms = {}

for i in range(K_CLUSTERS):
    center = kmeans.cluster_centers_[i]
    top_indices = center.argsort()[::-1][:5]  # 5 termos principais
    top_terms = [terms[j] for j in top_indices]
    cluster_top_terms[i] = ", ".join(top_terms)

print("\n✔ Termos principais por cluster (use isso para dar nome às categorias):")
for cid, palavras in cluster_top_terms.items():
    print(f"Cluster {cid}: {palavras}")


# =========================================================
# 7. Criar coluna de categoria automática
# =========================================================

# Aqui, por padrão, vamos usar a própria lista de termos como "nome da categoria".
# Depois você pode voltar e substituir por nomes mais bonitos manualmente.
df['CategoriaAutomatica'] = df['Cluster'].map(cluster_top_terms)


# =========================================================
# 8. Salvar resultado
# =========================================================

print(f"\n➡ Salvando arquivo categorizado em: {OUTPUT_FILE}")
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print("✔ Processo concluído.")
