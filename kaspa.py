
import requests
import time
import asyncio
import telegram
import os

# === CONFIGURACIÓN (segura) ===
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_USER_ID = int(os.getenv('TELEGRAM_USER_ID'))
CRYPTOPANIC_API_KEY = os.getenv('CRYPTOPANIC_API_KEY')

KEYWORDS = ["listing", "binance", "coinbase", "exchange", "partnership", "launch", "kaspa", "kas"]

CRYPTO_API_URL = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&currencies=kas&filter=important"

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

sent_news_ids = set()

def get_news():
    try:
        response = requests.get(CRYPTO_API_URL)
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"Error obteniendo noticias: {e}")
        return []

def filter_news(news):
    filtered = []
    for item in news:
        title = item.get('title', '').lower()
        url = item.get('url', '')
        news_id = item.get('id')
        if any(keyword in title for keyword in KEYWORDS):
            if news_id not in sent_news_ids:
                filtered.append((title, url, news_id))
    return filtered

async def send_news(news_list):
    for title, url, news_id in news_list:
        message = f"📰 *Noticia Importante de Kaspa*\n\n*{title.title()}*\n\n🔗 [Ver noticia]({url})"
        try:
            await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN)
            sent_news_ids.add(news_id)
            print(f"Enviado: {title}")
        except Exception as e:
            print(f"Error enviando noticia: {e}")

async def main():
    while True:
        print("🔎 Buscando noticias...")
        news = get_news()
        important_news = filter_news(news)
        if important_news:
            await send_news(important_news)
        await asyncio.sleep(300)  # Espera 5 minutos antes de revisar de nuevo

if __name__ == "__main__":
    asyncio.run(main())
