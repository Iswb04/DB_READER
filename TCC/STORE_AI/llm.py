
# irm https://ollama.com/install.ps1 | iex
# pip install langchain-community
# ollama run llama3
# python -m TCC.main

from langchain_ollama import OllamaLLM

llm_sql = OllamaLLM(model="llama3.1", temperature=0)
llm_exp = OllamaLLM(model="llama3.1", temperature=0.5)

def gerar_sql(pergunta):

    prompt = f"""
    Você é um especialista em SQL.

    Tabela vendas(produto, preco, quantidade)
    - Proibido mostrar e proibido oferecer ajuda para criar qualquer query que não seja SELECT.

    Pergunta: {pergunta}

    - Caso sejam perguntas como saudação (ex: "oi", "olá") ou conversa fiada ("ex: como você está", "tudo bem?"), NÃO RETORNE NADA.
    - Caso contrário, retorne APENAS UMA QUERY SQL VÁLIDA PARA MY SQL.

    """
    resposta = llm_sql.invoke(prompt)

    return resposta.replace("```sql", "").replace("```", "").strip()


def explicar(dados):
    prompt = f"""
    Analise os dados abaixo de forma simples, e explique em português:

    - insights básicos

    Dados:
    {dados}
    """
    return llm_exp.invoke(prompt)