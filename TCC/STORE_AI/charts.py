# pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt

def gerar_grafico(colunas, dados):
    df = pd.DataFrame(dados, columns=colunas)

    if len(df.columns) >= 2:
        df.plot(kind="bar")
        plt.title("Análise de Dados")
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.show()

    return df