import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from utils.pdf_extract import extract_text
from utils.pdf_create import create_pdf
import openai   # Gemini AI API compatible

OPENAI_API_KEY = "YOUR_GEMINI_API_KEY"
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me your English PDF test paper and I will translate it to Gujarati without watermark.")

def translate_text(text):
    prompt = f"Translate the following English text **word-to-word** into Gujarati:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gemini-1",  # Gemini AI model
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def handle_pdf(update: Update, context: CallbackContext):
    file = update.message.document.get_file()
    file.download("input.pdf")

    # Extract PDF text
    text = extract_text("input.pdf")

    # Translate using Gemini AI
    translated_text = translate_text(text)

    # Create new PDF
    create_pdf(translated_text, "translated.pdf")

    # Send PDF back to user
    update.message.reply_document(document=open("translated.pdf", "rb"))

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.Document.FileExtension("pdf"), handle_pdf))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
