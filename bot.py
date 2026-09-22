
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BOT SEGNALI ONLINE")

    def log_message(self, format, *args):
        pass

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🟢 BOT SEGNALI ONLINE\n\n"
        "Sistema in fase di configurazione.\n\n"
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
        "Il bot Telegram funziona correttamente."
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN non configurato")

    threading.Thread(target=start_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("test", test))

    print("Bot avviato...")
    app.run_polling()

if _name_ == "_main_":

    main()
