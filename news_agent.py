import requests
import os
from twilio.rest import Client

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

def get_kannada_news():
    API_KEY = os.getenv("NEWSDATA_API")

    if not API_KEY:
        return "❌ API key not found"

    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&language=kn&country=in"

    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        print("API response received")
    except Exception as e:
        return f"❌ API request failed: {str(e)}"

    results = data.get("results", [])

    print("Total results:", len(results))

    if not isinstance(results, list) or len(results) == 0:
        return "❌ No news available."

    msg = "📰 ಕಲಬುರಗಿ ಪ್ರಮುಖ ಸುದ್ದಿ\n\n"

    kalaburagi_news = []

    for article in results:
        title = article.get("title", "")
        description = article.get("description", "")
        link = article.get("link", "")

        print("Checking:", title)

        if not link:
            continue

        text = (title + " " + description).lower()

        if (
            "kalaburagi" in text
            or "gulbarga" in text
            or "ಕಲಬುರಗಿ" in text
            or "ಕಲಬುರಗಿಯಲ್ಲಿ" in text
            or "ಕಲಬುರಗಿಯ" in text
        ):
            print("Matched Kalaburagi:", title)
            short_link = shorten_url(link)
            kalaburagi_news.append((title, short_link))

        if len(kalaburagi_news) >= 7:
            break

    if len(kalaburagi_news) == 0:
        return "❌ ಇಂದು ಕಲಬುರಗಿ ಸಂಬಂಧಿಸಿದ ಸುದ್ದಿ ಲಭ್ಯವಿಲ್ಲ."

    count = 1
    for title, link in kalaburagi_news:
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
