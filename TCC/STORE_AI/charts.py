import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from itertools import count
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d")

def gerar_grafico(colunas, dados):
    df = pd.DataFrame(dados, columns=colunas)

    if len(df.columns) >= 2:
        pasta_destino = "DOWNLOADS"
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        for i in count(1):
            caminho_arquivo = os.path.join(pasta_destino, f"grafico{i}_{timestamp}.png")
            if not os.path.exists(caminho_arquivo):
                break 


        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        grafico = sns.barplot(
            data=df, 
            x=df.columns[0], 
            y=df.columns[1], 
            hue=df.columns[0],
            palette="viridis"
        )

        plt.title(f"Análise de Dados - Gráfico {i}", fontsize=15)
        plt.xlabel(df.columns[0].capitalize())
        plt.ylabel(df.columns[1].capitalize())
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(caminho_arquivo)
        plt.close()
        
        print(f"Gráfico salvo com sucesso em: {caminho_arquivo}")

    return df