import sqlite3

db_path = 'keys.db'

def list_keys():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys')
    keys = cursor.fetchall()

    if keys:
        print("Chaves no banco de dados:")
        for key in keys:
            print(f"Key: {key[0]}, Usada: {key[1]}")
    else:
        print("Nenhuma chave encontrada.")

    conn.close()

if __name__ == "__main__":
    list_keys()
