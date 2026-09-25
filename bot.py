import os
import threading
import asyncio
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


TOKEN = os.environ.get("BOT_TOKEN")
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY")
PORT = int(os.environ.get("PORT", "10000"))

FOOTBALL_API_URL = "https://v3.football.api-sports.io/status"


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


def check_football_api():
    if not FOOTBALL_API_KEY:
        return False, "FOOTBALL_API_KEY non configurata"

    try:
        request = Request(
            FOOTBALL_API_URL,
            headers={
                "x-apisports-key": FOOTBALL_API_KEY
            }
        )

        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("response") is not None:
            return True, "OK"

        errors = data.get("errors")

        if errors:
            return False, str(errors)

        return False, "Risposta API non valida"

    except HTTPError as e:
        return False, f"HTTP {e.code}"

    except URLError as e:
        return False, f"Connessione: {e.reason}"

    except Exception as e:
        return False, str(e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🟢 BOT SEGNALI ONLINE\n\n"
        "Sistema in fase di configurazione.\n\n"
        "/status - stato del bot\n"
        "/test - test funzionamento"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    api_ok, api_message = await asyncio.to_thread(check_football_api)

    if api_ok:
        calcio = "🟢 Dati calcio: COLLEGATI"
    else:
        calcio = "🔴 Dati calcio: NON COLLEGATI"

    await update.message.reply_text(
        "🟢 Sistema operativo\n"
        "📡 Monitoraggio: in configurazione\n"
        f"⚽ {calcio}\n"
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

    threading.Thread(
        target=start_server,
        daemon=True
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("test", test))

    print("Bot avviato...")

    app.run_polling()


if _name_ == "_main_":
    main()
