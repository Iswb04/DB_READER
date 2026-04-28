from TCC.DB.create import criar_banco
from TCC.DB.itens import inserir_item

criar_banco()

# Inserir dados (rodar só uma vez)
dados = [
    ("Notebook", 3500, 1),
    ("Mouse", 120, 2),
    ("Teclado", 250, 1),
    ("Monitor", 900, 1),
    ("Headset", 300, 1),
    ("Celular", 2200, 1),
    ("Carregador", 80, 3),
    ("HD Externo", 400, 1),
    ("Caixa de Som", 350, 1),
    ("Webcam", 200, 1)
]

for item in dados:
    inserir_item(*item)

# python -m TCC.DB.run