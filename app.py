from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, filters
import logging
from database import Database

user_status = {}

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# Produtos para cada painel
product_lists = {
    'painel1': [
        ("Memória RAM SUPERHEER DDR3, 24GB (3x8) 1600MHz", "R$63", "EXTRA20OFF", "649 Moedas no APP + Google Pay", "https://a.aliexpress.com/_oCRery5"),
    ],
    'painel2': [
        ("SSD Walram SATA 500GB", "R$93", "EXTRA20OFF", "714 Moedas no APP + Google Pay", "https://a.aliexpress.com/_oDlANsV"),
        ("SSD Walram SATA 1TB", "R$199", "IFP5MXK", "1018 Moedas no APP + Google Pay", "https://a.aliexpress.com/_oDlANsV"),
    ],
    # Adicione outros painéis e produtos conforme necessário
}

# Inicialize o banco de dados
db = Database('keys_db.sqlite')
db.create_keys_table()

def add_key(key):
    db.add_key(key)  # Adicione a chave à tabela

# Comando /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Adquirir Key", url="https://t.me/puropg")],
        [InlineKeyboardButton("Resgatar Key", callback_data='redeem')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"Olá {user.first_name}, adquira sua key de acesso ao bot de salas com @puropg.",
        reply_markup=reply_markup
    )

# Comando /painel
async def painel(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_status.get(user_id, False):
        keyboard = [
            [InlineKeyboardButton("Painel 1", callback_data='painel1')],
            [InlineKeyboardButton("Painel 2", callback_data='painel2')],
            [InlineKeyboardButton("Painel 3", callback_data='painel3')],
            [InlineKeyboardButton("Painel 4", callback_data='painel4')],
            [InlineKeyboardButton("Painel 5", callback_data='painel5')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message:
            await update.message.reply_text("Clique no botão abaixo para acessar os painéis", reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.message.edit_text("Clique no botão abaixo para acessar os painéis", reply_markup=reply_markup)
    else:
        if update.message:
            await update.message.reply_text("Você precisa resgatar uma key válida para acessar os painéis.")
        elif update.callback_query:
            await update.callback_query.message.edit_text("Você precisa resgatar uma key válida para acessar os painéis.")

# Resgate de key via botão
async def redeem_key(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Envie sua key:")
    context.user_data['awaiting_key'] = True

# Processar key enviada pelo usuário
async def handle_key(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_key'):
        key = update.message.text
        user_id = update.effective_user.id

        if db.validate_key(key):
            db.use_key(key)
            user_status[user_id] = True
            await update.message.reply_text("Key resgatada com sucesso.")
            await painel(update, context)  # Mostrar o menu de painéis após resgatar a key
        else:
            await update.message.reply_text("Key inválida ou já utilizada.")
        context.user_data['awaiting_key'] = False

# Mostrar produtos do painel selecionado
async def show_products(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    painel = query.data
    products = product_lists.get(painel, [])

    if products:
        product_text = "\n\n".join(
            f"===============================\n\n{prod[0]}\n\n💲 Valor: {prod[1]}\n-Cupom: {prod[2]} + {prod[3]}\n👀 {prod[4]}"
            for prod in products
        )
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data='close_list')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edita a mensagem existente para mostrar os produtos
        await query.edit_message_text(product_text, reply_markup=reply_markup)
    else:
        # Se não houver produtos, informa o usuário e adiciona o botão de voltar
        keyboard = [
            [InlineKeyboardButton("Voltar", callback_data='close_list')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Nenhum produto disponível para este painel.", reply_markup=reply_markup)

# Fechar lista e retornar ao menu de painéis
async def close_list(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await painel(update, context)  # Retornar ao menu de painéis

# Voltar ao menu principal
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await painel(update, context)  # Voltar ao menu de painéis

def main():
    application = Application.builder().token("6953201006:AAHLLa8j1hT0jI7_4rVpH2E8nh2cWMhWJJI").build()

    # Adicione handlers para comandos e callbacks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("painel", painel))
    application.add_handler(CallbackQueryHandler(redeem_key, pattern='redeem'))
    application.add_handler(CallbackQueryHandler(show_products, pattern='painel[1-5]'))
    application.add_handler(CallbackQueryHandler(close_list, pattern='close_list'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='back'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_key))

    application.run_polling()

if __name__ == '__main__':
    main()
