import requests
import os
from twilio.rest import Client

def get_kannada_news():
    API_KEY = os.getenv("NEWSDATA_API")
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&language=kn&country=in"

    res = requests.get(url).json()
    articles = res.get("results", [])[:5]

    msg = "📰 ಇಂದಿನ ಪ್ರಮುಖ ಕನ್ನಡ ಸುದ್ದಿ\n\n"

    for i, article in enumerate(articles, 1):
        title = article.get("title", "ಸುದ್ದಿ ಶೀರ್ಷಿಕೆ ಲಭ್ಯವಿಲ್ಲ")
        link = article.get("link", "")

        msg += f"{i}. {title}\n{link}\n\n"

    msg += "ಶುಭೋದಯ ☀️"
    return msg


def send_whatsapp(message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    client = Client(account_sid, auth_token)

    client.messages.create(
        from_="whatsapp:+14155238886",  # Twilio sandbox number
        body=message,
        to=os.getenv("TWILIO_WHATSAPP_TO")
    )


if __name__ == "__main__":
    news = get_kannada_news()
    send_whatsapp(news)
