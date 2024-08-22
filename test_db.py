from database import Database

# Inicializa a classe Database com o caminho do banco de dados
db = Database('keys.db')

# Cria a tabela se ainda não existir
db.create_keys_table()

# Adiciona uma nova chave para testar
db.add_key('key123')

# Tenta validar a chave
if db.validate_key('minha-chave'):
    print("Chave válida!")
    db.use_key('minha-chave')  # Marca a chave como usada
else:
    print("Chave inválida ou já usada.")

# Simula o reinício da aplicação tentando validar a chave novamente
if db.validate_key('minha-chave'):
    print("Chave válida!")
else:
    print("Chave inválida ou já usada.")
