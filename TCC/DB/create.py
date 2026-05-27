import mysql.connector

def conectar(banco=None):
    """Estabelece a conexão com o MySQL. 
    Aceita o nome do banco como opcional para permitir a criação dele."""
    config = {
        "host": "localhost",
        "user": "app",
        "password": "1234"
    }
    
    # adiciona nas configurações do banco
    if banco:
        config["database"] = banco
        
    return mysql.connector.connect(**config) #desempacotador de dic


def criar_banco():
    con = conectar()
    cursor = con.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS store")
    cursor.execute("USE store")
    cursor.execute("SHOW TABLES LIKE 'vendas'")

    # se o retorno for não for vazio, a tabela já existe
    resultado = cursor.fetchone()

    if resultado:
        print("A tabela 'vendas' já existe! (ou você inseriu dados!)")
    else:
        cursor.execute("""
        CREATE TABLE vendas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            produto VARCHAR(100),
            preco DECIMAL(10,2),
            marca VARCHAR(100),
            modelo VARCHAR(100),
            quantidade INT
        )
        """)
        print("Tabela 'vendas' criada com sucesso!")

    con.commit()
    con.close()

# executar direto do terminal
if __name__ == "__main__":
    criar_banco()