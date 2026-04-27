
# irm https://ollama.com/install.ps1 | iex
# pip install langchain-community
# ollama run llama3

from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def gerar_sql(pergunta):
    prompt = f"""
    Você é um especialista em SQL.

    Tabela vendas(produto, preco, quantidade)

    Gere uma query SQL válida para MySQL.

    Pergunta: {pergunta}

    Retorne apenas a SQL.
    """
    resposta = llm.invoke(prompt)

    return resposta.replace("```sql", "").replace("```", "").strip()


def explicar(dados):
    prompt = f"""
    Analise os dados abaixo e explique em português:

    - insights
    - possíveis motivos

    Dados:
    {dados}
    """
    return llm.invoke(prompt)