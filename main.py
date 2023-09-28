import os
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from src.middleware.authentication import authorization
from src.controller.lancamento_controller import handle_start_lancamento, handle_stop_lancamento, handle_status_lancamento

load_dotenv()

app = Client(
    name="LANÇAMENTO_BOT", 
    api_hash=os.getenv("API_HASH_TELEGRAM"),
    api_id=os.getenv("API_ID_TELEGRAM"),
    bot_token=os.getenv("BOT_TOKEN_TELEGRAM_LANCAMENTO")
    )

@app.on_message(filters.command("start"))
def lancamento(client, message: Message):
    message.reply_text(f"""
/lancamento - Setor lancamento
/chat - Informa seu _id
/group - Informa _id grupo
""")

@app.on_message(filters.command("lancamento"))
@authorization()
def financeiro(client, message: Message):
    message.reply_text(f"""
/iniciar_lancamento - Iniciar lancamento
/parar_lancamento - Parar lancamento
/status_lancamento - Status lancamento
""")

@app.on_message(filters.command("group"))
@authorization()
def handle_group_id(client: Client, message: Message):
    client.send_message(int(os.getenv("CHAT_ID_ADM")), message)

@app.on_message(filters.command("chat"))
def handle__id(client: Client, message: Message):
    text = f"{message.chat.first_name}.{message.chat.last_name} - ID:{message.from_user.id}"
    client.send_message(message.from_user.id, text)
    if int(os.getenv("CHAT_ID_ADM")) != message.from_user.id:
        client.send_message(int(os.getenv("CHAT_ID_ADM")), text)

# iniciar Lançamento
@app.on_message(filters.command("iniciar_lancamento"))
@authorization()
def iniciar_lancamento(client: Client, message: Message):
    handle_start_lancamento(client, message)

# parar Lançamento
@app.on_message(filters.command("parar_lancamento"))
@authorization()
def parar_lancamento(client: Client, message: Message):
    handle_stop_lancamento(client, message)

# status Lançamento
@app.on_message(filters.command("status_lancamento"))
@authorization()
def status_lancamento(client: Client, message: Message):
    handle_status_lancamento(client, message)

print("Service Telegram Up!")
app.run()

