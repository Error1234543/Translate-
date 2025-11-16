import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.pdf_extract import extract_text
from utils.pdf_create import create_pdf

# Environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Gemini API key
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Telegram Bot token

if not GEMINI_API_KEY or not TELEGRAM_TOKEN:
    raise ValueError("ERROR: Please set GEMINI_API_KEY and TELEGRAM_TOKEN in environment variables!")

# Gemini API function
def translate_text_gemini(text):
    url = "https://gemini-api.openai.com/v1/chat/completions"  # Gemini-compatible endpoint
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-1",   # Gemini model
        "messages": [
            {"role": "user", "content": f"Translate the following English text word-to-word into Gujarati:\n\n{text}"}
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise error if request failed
    result = response.json()
    return result['choices'][0]['message']['content']

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me your English PDF test paper and I will translate it to Gujarati using Gemini AI."
    )

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    await file.download_to_drive("input.pdf")

    # Extract PDF text
    text = extract_text("input.pdf")

    # Translate using Gemini API
    try:
        translated_text = translate_text_gemini(text)
    except Exception as e:
        await update.message.reply_text(f"Translation failed: {str(e)}")
        return

    # Create new PDF
    create_pdf(translated_text, "translated.pdf")

    # Send PDF back to user
    await update.message.reply_document(document=open("translated.pdf", "rb"))

# Main bot function
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.FileExtension("pdf"), handle_pdf))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()