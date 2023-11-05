import logging
import const as key
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import telegram
import openai

openai.api_key = key.CHAT_GPT_TOKEN
youtube = build("youtube", "v3", developerKey=key.YOUTUBE_TOKEN)
bot = telegram.Bot(token=key.TELEGRAM_TOKEN)

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
            await context.bot.send_message(chat_id, "Sorry :(, I couldn't find an image for that word. Try again!") 


# Function to handle YouTube video search
async def search_youtube_video(update: Update, context: CallbackContext):
    print('Searching for video...')
    if update.message.text.startswith('/search_youtube'):
        query = update.message.text[len('/search_youtube'):].strip()
        chat_id = update.message.chat.id

        try:
            search_response = youtube.search().list(
                q=query,
                type="video",
                part="id",
                maxResults=1  # You can adjust this to control the number of results.
            ).execute()

            if "items" in search_response:
                video_id = search_response["items"][0]["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await bot.send_message(chat_id=chat_id, text=video_url)
            else:
                await context.bot.send_message(chat_id, "Sorry :(, I couldn't find a video on YouTube. Try again!")
        except HttpError as e:
            print(f"HTTP error: {e}")
            await context.bot.send_message(chat_id, "Sorry :(, there was an error while searching for YouTube videos. Please try again!")


#gpt handler
async def gpt_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    print('Thinking...')
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=user_input,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,  
        presence_penalty=0.0  
    )
    bot_response = response.choices[0].text
    update.message.reply_text(bot_response) 