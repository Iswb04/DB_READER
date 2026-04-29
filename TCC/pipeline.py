from TCC.STORE_AI.llm import gerar_sql, explicar
from TCC.DB.create import conectar
from TCC.STORE_AI.charts import gerar_grafico
from TCC.STORE_AI.exports import salvar_csv


def rodar_pipeline(pergunta):

    # 1. IA gera SQL
    sql = gerar_sql(pergunta)
    print("Resposta:", sql)

    # 2. valida segurança
    if not sql.lower().strip().startswith("select"):
        return "Apenas consultas SELECT são permitidas."

    # 3. conecta no banco
    con = conectar()
    cursor = con.cursor()

    try:
        # 4. executa SQL (ÚNICO lugar correto)
        cursor.execute(sql)

        if cursor.description:
            colunas = [desc[0] for desc in cursor.description]
            dados = cursor.fetchall()
        else:
            colunas = []
            dados = []

        con.close()

    except Exception as e:
        con.close()
        print("\033[31mOcorreu um erro. Por favor, reformule sua pergunta.\033[0m")
        print(f"\033[31mErro técnico:\033[0m {e}")
        return None

    # 5. formata dados
    dados_formatados = [
        dict(zip(colunas, linha)) for linha in dados
    ]

    # 6. gráfico
    if input("Gerar gráfico? (S ou N): ").upper() in ["S", "SIM"]:
        gerar_grafico(colunas, dados)

    # 7. CSV
    if input("Exportar CSV? (S ou N): ").upper() in ["S", "SIM"]:
        salvar_csv(colunas, dados)

    # 8. explicação da IA
    resposta = explicar(dados_formatados)

    return resposta