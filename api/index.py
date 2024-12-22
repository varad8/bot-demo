import os
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")


app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.dict(), bot)  # Convert the Telegram Webhook class to dictionary using dict() method

    # Create an application and register handlers
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    # Handle webhook request
    await application.process_update(update)

    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}