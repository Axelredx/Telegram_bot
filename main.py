import engine as eng
import logging
import const as key
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import requests
import telegram
import openai

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Axe at your service!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im an Axe! I can do many things such as cut or search for images/video!')

#responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hi there!'
    elif 'how are you?' in processed:
        return 'Great! Hope you too!'
    elif 'time' in processed:
        now = datetime.now()
        date_time = now.strftime('%d/%m/%y, %H:%M:%S')
        return str(date_time)
    else:
        return 'sorry i didnt understand :( ...can you repeat please??'

#debug
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    #bot in grup chat
    if message_type == 'group':
        if key.BOT_USERNAME in text:
            new_text: str = text.replace(key.BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

#error
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {Update} caused error: {context.error}')
    

def main():
    print('Bot is running...')
    app = Application.builder().token(key.TELEGRAM_TOKEN).build()
    
    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler("search_image", eng.search_image_command))
    app.add_handler(CommandHandler("help_image", eng.help_image_command))
    app.add_handler(CommandHandler('search_youtube', eng.search_youtube_video))
    
    #messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #app.add_handler(MessageHandler(filters.TEXT , eng.gpt_message)) need to pay for working api
    
    #errors
    app.add_error_handler(handle_error)
    
    #check for new messages
    #print('Polling for messages...')
    app.run_polling(poll_interval=1)   #1sec interval 

if __name__ == '__main__':
    main()