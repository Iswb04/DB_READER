import os
import pandas as pd
from itertools import count
from datetime import datetime



def salvar_csv(df):
    pasta_destino = "TCC/DOWNLOADS"
    timestamp = datetime.now().strftime("%Y%m%d")

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)


    for i in count(1):
        nome = f"dados{i}_{timestamp}.csv"
        caminho_completo = os.path.join(pasta_destino, nome)
        
        if not os.path.exists(caminho_completo):
            break 

    df.to_csv(caminho_completo, index=False)
    print(f"CSV salvo com sucesso em: {caminho_completo}")

