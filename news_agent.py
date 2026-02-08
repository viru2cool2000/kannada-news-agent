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

    results = data.get("results", [])

    if not isinstance(results, list) or len(results) == 0:
        return "❌ No news available."

    msg = "📰 ಇಂದಿನ ಪ್ರಮುಖ ಕನ್ನಡ ಸುದ್ದಿ\n\n"

    kalaburagi_news = []
    general_news = []

    for article in results:
        title = article.get("title", "")
        link = article.get("link", "")

        if not link:
            continue

        short_link = shorten_url(link)

        if (
            "kalaburagi" in title.lower()
            or "gulbarga" in title.lower()
            or "ಕಲಬುರಗಿ" in title
        ):
            if len(kalaburagi_news) < 2:
                kalaburagi_news.append((title, short_link))
        else:
            if len(general_news) < 7:
                general_news.append((title, short_link))

        if len(kalaburagi_news) >= 2 and len(general_news) >= 7:
            break

    # If not enough Kalaburagi news, fill from general
    while len(kalaburagi_news) < 2 and general_news:
        kalaburagi_news.append(general_news.pop(0))

    count = 1

    msg += "📍 ಕಲಬುರಗಿ ಸುದ್ದಿ\n\n"
    for title, link in kalaburagi_news:
        msg += f"{count}. {title}\n{link}\n\n"
        count += 1

    msg += "🗞 ಪ್ರಮುಖ ರಾಜ್ಯ/ದೇಶ ಸುದ್ದಿ\n\n"
    for title, link in general_news[:5]:
        msg += f"{count}. {title}\n{link}\n\n"
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
    news = get_kannada_news()
    print(news)  # visible in GitHub logs
    send_whatsapp(news)
