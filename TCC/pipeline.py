from STORE_AI.llm import gerar_sql, explicar
from DB.create import conectar
from STORE_AI.charts import gerar_grafico
from STORE_AI.exports import salvar_csv

def rodar_pipeline(pergunta):

    # 1. IA gera SQL
    sql = gerar_sql(pergunta)
    print("SQL gerado:", sql)

    # 2. Executa no banco
    con = conectar()
    cursor = con.cursor()

    cursor.execute(sql)
    dados = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    con.close()

    # 3. Gera gráfico
    question = input("Gerar gráfico? (S ou N): ").upper()
    if question in ["SIM", "S"]:
        df = gerar_grafico(colunas, dados)
    else:
        print("ok.")

    # 4. Exporta CSV
    question2 = input("Exportar CSV? (S ou N): ").upper()
    if question2 in ["SIM", "S"]:
        salvar_csv(df)
    else:
        print("ok.")

    # 5. IA explica
    resposta = explicar(df)

    return resposta