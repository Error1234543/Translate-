import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from utils.pdf_extract import extract_text
from utils.pdf_create import create_pdf
import openai   # Gemini AI API compatible

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me your English PDF test paper and I will translate it to Gujarati without watermark."
    )

def translate_text(text):
    prompt = f"Translate the following English text **word-to-word** into Gujarati:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gemini-1",  # Gemini AI model
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    await file.download_to_drive("input.pdf")

    # Extract PDF text
    text = extract_text("input.pdf")

    # Translate using Gemini AI
    translated_text = translate_text(text)

    # Create new PDF
    create_pdf(translated_text, "translated.pdf")

    # Send PDF back to user
    await update.message.reply_document(document=open("translated.pdf", "rb"))

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.FileExtension("pdf"), handle_pdf))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()