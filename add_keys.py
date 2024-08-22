import sqlite3

def add_key(key):
    conn = sqlite3.connect('keys_db.sqlite')
    c = conn.cursor()

    # Cria a tabela se não existir
    c.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            used BOOLEAN NOT NULL
        )
    ''')

    # Insere a chave no banco de dados
    try:
        c.execute('INSERT INTO keys (key, used) VALUES (?, ?)', (key, False))
        conn.commit()
        print(f"Chave '{key}' adicionada com sucesso.")
    except sqlite3.IntegrityError:
        print(f"A chave '{key}' já existe.")
    finally:
        conn.close()

if __name__ == '__main__':
    key = input("Digite a chave para adicionar: ")
    add_key(key)
