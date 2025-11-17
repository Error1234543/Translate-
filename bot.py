from telebot import TeleBot
import os
from googletrans import Translator

# Import helper modules
from utilise.extract import extract_text_from_pdf
from utilise.create import create_pdf_from_text

# ====== Bot Config ======
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ Please set TELEGRAM_TOKEN in environment variables!")

bot = TeleBot(TELEGRAM_TOKEN)
translator = Translator()

# ====== Translation Function ======
def translate_text(text, dest_language='gu'):
    return translator.translate(text, src='auto', dest=dest_language).text

# ====== Start Command ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hello! Send me any PDF, I will translate it to Gujarati and send it back.")

# ====== PDF Handler ======
@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_pdf_path = f"input_{message.from_user.id}.pdf"
        with open(input_pdf_path, 'wb') as f:
            f.write(downloaded_file)

        # Extract text
        text = extract_text_from_pdf(input_pdf_path)

        # Translate text
        translated_text = translate_text(text)

        # Create PDF
        output_pdf_path = f"translated_{message.from_user.id}.pdf"
        create_pdf_from_text(translated_text, output_pdf_path)

        # Send translated PDF
        with open(output_pdf_path, 'rb') as f:
            bot.send_document(message.chat.id, f)

        # Clean up
        os.remove(input_pdf_path)
        os.remove(output_pdf_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# ====== Run Bot ======
bot.infinity_polling()