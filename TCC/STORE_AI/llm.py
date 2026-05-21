
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

    REGRAS ABSOLUTAS:
    - Caso seja uma saudação ou conversa fiada, retornar apenas: INVALID
    - Caso não contenha na tabela, gere o SQL e avise que não tem: INVALID
    - Responda SOMENTE com uma query SQL
    - SEM explicações
    - SEM texto extra
    - SEM markdown
    - SEM comentários
    - Apenas 1 linha
    - Apenas SELECT

    Tabela vendas(produto, preco, quantidade)

    Pergunta: {pergunta}

    """
    resposta = llm_sql.invoke(prompt)

    return resposta.replace("```sql", "").replace("```", "").strip()


def explicar(dados):
    prompt = f"""
    Analise os dados abaixo, e explique em UM PARÁGRAFO em português:

    - insights básicos

    Dados:
    {dados}
    """
    return llm_exp.invoke(prompt)