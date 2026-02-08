import requests
import os
from twilio.rest import Client


def get_kannada_news():
    API_KEY = os.getenv("NEWSDATA_API")

    if not API_KEY:
        return "❌ API key not found"

    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&language=kn&country=in"

    try:
        response = requests.get(url, timeout=15)
        data = response.json()
    except Exception as e:
        return f"❌ API request failed: {str(e)}"

    msg = "📰 ಇಂದಿನ ಪ್ರಮುಖ ಕನ್ನಡ ಸುದ್ದಿ\n\n"

    results = data.get("results", [])

    if not isinstance(results, list) or len(results) == 0:
        return f"❌ No news available.\nAPI Response: {data}"

    for i, article in enumerate(results[:5], 1):
        title = article.get("title", "ಸುದ್ದಿ ಶೀರ್ಷಿಕೆ ಲಭ್ಯವಿಲ್ಲ")
        link = article.get("link", "")

        msg += f"{i}. {title}\n{link}\n\n"

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
    news = get_kannada_news()
    print(news)  # visible in GitHub logs
    send_whatsapp(news)
