from TCC.IA.llm import gerar_sql, explicar
from TCC.DB.create import conectar
from TCC.IA.charts import gerar_grafico
from TCC.IA.exports import salvar_csv

def rodar_pipeline(pergunta):
    print("\nPergunta:", pergunta)

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
    df = gerar_grafico(colunas, dados)

    # 4. Exporta CSV (opcional)
    salvar_csv(df)

    # 5. IA explica
    resposta = explicar(df)

    return resposta