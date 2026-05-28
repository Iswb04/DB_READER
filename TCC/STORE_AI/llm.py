
# irm https://ollama.com/install.ps1 | iex
# pip install langchain-community
# ollama run llama3
# python -m TCC.main

from langchain_ollama import OllamaLLM

llm_sql = OllamaLLM(model="llama3.1", temperature=0)
llm_exp = OllamaLLM(model="llama3.1", temperature=0.5)

def gerar_sql(pergunta):
    prompt = f"""

    Você é um tradutor de linguagem natural para consultas SQL puro do MySQL. Sua única função é transformar a pergunta do usuário em um comando SQL baseado na tabela 'vendas'.

    ESTRUTURA DA TABELA 'vendas':
    - produto (VARCHAR)
    - preco (DECIMAL)
    - marca (VARCHAR)
    - modelo (VARCHAR)
    - quantidade (INT)

    REGRAS ABSOLUTAS:
    - Caso seja uma saudação ou conversa fiada, retornar apenas: INVALID
    - Responda SOMENTE com uma query SQL válida, sem blocos de código markdown ou aspas.
    - SEM explicações, SEM texto extra, SEM comentários, em apenas 1 linha e utilizando apenas SELECT.
    - Se a intenção do usuário não for um comando de seleção (SELECT), retornar apenas: INVALID
    - Se o usuário digitar por exemplo "mouse multilaser", saiba que "mouse" é o produto e "multilaser" é a marca.
    - Se a busca for pela quantidade de itens de uma marca ou categoria, use obrigatoriamente o GROUP BY seguindo o exemplo: SELECT produto, SUM(quantidade) FROM vendas WHERE marca = 'Samsung' GROUP BY produto
    - Se o usuário quiser listar o produto, a quantidade individual e a soma total de todos os itens juntos na mesma busca, utilize a função de janela: SELECT produto, quantidade, SUM(quantidade) OVER() AS quantidade_total FROM vendas
    - Quando for informado que o banco de dados retornou uma lista vazia, sua única função é gerar uma frase curta e clara avisando que não há itens com essa característica disponível no momento.

    Tabela vendas(produto, preco, marca, modelo, quantidade)

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