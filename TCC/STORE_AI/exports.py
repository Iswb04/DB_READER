import os
import csv
from itertools import count
from datetime import datetime

def salvar_csv(colunas, dados):
    pasta = "TCC/DOWNLOADS"
    os.makedirs(pasta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")

    for i in count(1):
        caminho = os.path.join(pasta, f"dados{i}_{timestamp}.csv")
        if not os.path.exists(caminho):
            break

    with open(caminho, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colunas)
        writer.writerows(dados)

    print(f"CSV salvo em: {caminho}")