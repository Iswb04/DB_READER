import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="app",
        password="1234",
        database="store"
    )

def criar_banco():
    con = mysql.connector.connect(
        host="localhost",
        user="app",
        password="1234"
    )
    cursor = con.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS store")
    cursor.execute("USE store")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        produto VARCHAR(100),
        preco DECIMAL(10,2),
        quantidade INT
    )
    """)

    con.commit()
    con.close()

    print("Banco pronto!")