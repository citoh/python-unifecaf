# INSTALANDO A APLICAÇÃO:
# python3 -m venv venv
# source venv/bin/activate
# pip install mysql-connector-python

import mysql.connector

# Configuração da conexão
config = {
    "host": "localhost",   # ou IP do servidor
    "user": "root",        # ex: root
    "password": "root",    # senha do MySQL
    "database": "unifecaf" # banco de dados já criado
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

try:
    # Conectando ao MySQL
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    print("Conexão realizada com sucesso!")

    # Criando tabela de exemplo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        email VARCHAR(100)
    )
    """)

    # Inserindo dados
    cursor.execute(
        "INSERT INTO usuarios (nome, email) VALUES (%s, %s)", 
        ("Ana", "ana@email.com")
    )
    conn.commit()

    # Consultando dados
    cursor.execute(
        "SELECT * FROM usuarios"
    )
    
    for row in cursor.fetchall():
        print(row)

except mysql.connector.Error as err:
    print(f"Erro: {err}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão encerrada.")