# ─────────── bot.py ───────────
import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TELEGRAM_TOKEN  = '7510483125:AAFgMF6ysMYbrT-_KxmIZKYJAPFBRIa7y8s'
YOUTUBE_API_KEY = 'AIzaSyAoIj0fgWquennVrhArFkzGUHtvwHHjDIc'

# URL where player.html is hosted via GitHub Pages
WEBAPP_BASE_URL = 'https://github.com/MesfinShimels/youtube/blob/main/player.html'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Use `/search <keywords>` to find videos and play in‑app."
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❗ Usage: /search <video keyword>")

    query = ' '.join(context.args)
    api_url = (
        'https://www.googleapis.com/youtube/v3/search'
        f'?part=snippet&q={requests.utils.requote_uri(query)}'
        f'&type=video&key={YOUTUBE_API_KEY}&maxResults=5'
    )
    items = requests.get(api_url).json().get('items', [])
    if not items:
        return await update.message.reply_text("😕 No results found.")

    for item in items:
        vid   = item['id']['videoId']
        title = item['snippet']['title']
        thumb = item['snippet']['thumbnails']['high']['url']
        webapp_url = f"{WEBAPP_BASE_URL}?vid={vid}"
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("▶️ Watch in‑app", web_app=WebAppInfo(url=webapp_url)),
            InlineKeyboardButton("🔗 YouTube", url=f"https://youtu.be/{vid}")
        ]])
        await update.message.reply_photo(photo=thumb, caption=title, reply_markup=kb)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "/start    - Welcome message\n"
        "/search   - Search YouTube and play in‑app\n"
        "/help     - Show this help message\n"
    )
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_command))
    app.add_handler(CommandHandler("search", search))
    print("✅ Bot is running…")
    app.run_polling()

if __name__ == '__main__':
    main()
