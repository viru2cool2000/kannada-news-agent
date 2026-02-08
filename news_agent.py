import requests
import os
from twilio.rest import Client
import feedparser
from datetime import datetime, timedelta


def shorten_url(long_url):
    try:
        short = requests.get(
            "https://tinyurl.com/api-create.php",
            params={"url": long_url},
            timeout=10
        )
        return short.text
    except:
        return long_url
import feedparser

def get_kalaburagi_news():
    url = "https://news.google.com/rss/search?q=Kalaburagi+OR+Kalburgi+OR+Kalaburgi+OR+Gulbarga&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(url)

    if not feed.entries:
        return "❌ ಸುದ್ದಿ ಲಭ್ಯವಿಲ್ಲ."

    msg = "📰 ಕಲಬುರಗಿ ಪ್ರಮುಖ ಸುದ್ದಿ\n\n"

    count = 1

    for entry in feed.entries[:7]:
        title = entry.title
        link = entry.link
        short_link = shorten_url(link)

        msg += f"{count}. {title}\n{short_link}\n\n"
        count += 1

    msg += "ಶುಭೋದಯ ☀️"
    return msg
    
def send_whatsapp(message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")
    to_number = os.getenv("TWILIO_WHATSAPP_TO")

    if not account_sid or not auth_token or not from_number or not to_number:
        print("❌ Twilio credentials missing")
        return

    client = Client(account_sid, auth_token)

    client.messages.create(
        from_=from_number,
        body=message,
        to=to_number
    )


if __name__ == "__main__":
    news = get_kalaburagi_news()
    print(news)  # visible in GitHub logs
    send_whatsapp(news)
