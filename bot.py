python
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟢 BOT SEGNALI ONLINE\n\n"
        "Sistema in fase di configurazione.\n\n"
        "Comandi disponibili:\n"
        "/status - stato del bot\n"
        "/test - test di funzionamento"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟢 Sistema operativo\n"
        "📡 Monitoraggio: in configurazione\n"
        "⚽ Dati calcio: non ancora collegati\n"
        "📊 Motore segnali: non ancora attivo"
    )

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ TEST RIUSCITO\n\n"
        "Il bot Telegram sta funzionando correttamente."
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN non configurato")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("test", test))

    print("Bot avviato...")
    app.run_polling()

if _name_ == "_main_":
    main()
