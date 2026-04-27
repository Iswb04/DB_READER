from TCC.DB.create import conectar

def inserir_item(produto, preco, quantidade):
    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
    INSERT INTO vendas (produto, preco, quantidade)
    VALUES (%s, %s, %s)
    """, (produto, preco, quantidade))

    con.commit()
    con.close()

def listar_itens():
    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM vendas")

    for item in cursor.fetchall():
        print(item)

    con.close()