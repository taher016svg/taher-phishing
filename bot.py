from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, threading

TOKEN = "8845154239:AAELzzKtiQTrHYAf4KF5DdmI-hL-8oWS4ws"
CHAT_ID = 8860670510

async def start(update, context):
    await update.message.reply_text("Bot works")

async def test(update, context):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="this is a test message from bot")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            with open("index.html", "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length).decode())
        name = data.get("name", "")
        email = data.get("email", "")
        bot = Bot(token=TOKEN)
        import asyncio
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=f"New submission!\nName: {name}\nEmail: {email}"))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_server():
    server = HTTPServer(("0.0.0.0", 3000), Handler)
    print("Web server running on port 3000...")
    server.serve_forever()

def main():
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
