import sqlite3

# Nome do arquivo do banco de dados (será criado se não existir)
DB_NAME = "teste.db"

try:
    # Conectando ao SQLite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Conexão SQLite realizada com sucesso!")

    # Criando tabela de exemplo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT
    )
    """)

    # Inserindo dados
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", ("Ana", "ana@email.com"))
    conn.commit()

    # Consultando dados
    cursor.execute("SELECT * FROM usuarios")
    for row in cursor.fetchall():
        print(row)

except sqlite3.Error as err:
    print(f"Erro: {err}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexão encerrada.")