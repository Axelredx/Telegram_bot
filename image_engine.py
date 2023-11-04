import logging
import const as key
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests
import telegram

bot = telegram.Bot(token=key.TOKEN)
async def help_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Type "/search_image" + [word/s] to receive an image about what you asked!')

# Function to handle image search
async def search_image_command(update: Update, context: CallbackContext):
    # Check if the command is /search
    print('Searching...')
    if update.message.text.startswith('/search_image'):
        word = update.message.text[len('/search_image'):].strip()
        chat_id = update.message.chat.id 
        
        # Use the Pixabay API to search for images based on the word
        PIXABAY_API_KEY = key.SEARCH_TOKEN
        PIXABAY_API_URL = key.IMAGE_LINK

        params = {
            "key": PIXABAY_API_KEY,
            "q": word,
            "image_type": "photo",
        }

        response = requests.get(PIXABAY_API_URL, params=params)
        data = response.json()

        if data["hits"]:
            # Send the first image from the search results
            image_url = data["hits"][0]["webformatURL"]
            await context.bot.send_photo(chat_id, image_url)
            print('Image sent')  
        else:
            await context.bot.send_message(chat_id, "Sorry :(, I couldn't find an image for that word. Try again!")  # Use 'await' here

