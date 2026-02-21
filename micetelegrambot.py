# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

load_dotenv()

TOKEN = os.environ.get('TELEGRAM_TOKEN')

GAME_URL = "https://danilamax2608.github.io/MiceGame/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = "Greetings, little mouse. Your task is simple: eat as many pieces of cheese as possible."

    keyboard = [
        [InlineKeyboardButton("Start Game", web_app=WebAppInfo(url=GAME_URL))],
        [InlineKeyboardButton("How to play", callback_data='how_to_play')],
        [InlineKeyboardButton("About the game", callback_data='about_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'how_to_play':
        how_to_play_message = ("As you move through the rooms, you'll find pieces of cheese. "
                               "You need to eat as many of them as possible, faster than the other mice.")
        await query.edit_message_text(text=how_to_play_message, reply_markup=query.message.reply_markup)

    elif query.data == 'about_game':
        about_game_message = ("Mice is a multiplayer game. "
                              "You and several other players compete to see who can collect the most pieces of cheese. "
                              "When the timer runs out, the one who has eaten the most pieces of cheese wins.")
        await query.edit_message_text(text=about_game_message, reply_markup=query.message.reply_markup)

def run_http_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

def main() -> None:
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
