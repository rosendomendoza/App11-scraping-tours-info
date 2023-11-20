import smtplib, ssl, os
import requests
from datetime import datetime

EMAIL_PASSWORD = os.getenv("PASSWORD")

NEWS_API_KEY = os.getenv("NEWSAPIKEY")

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "profesor.rosendo@gmail.com"
    password = EMAIL_PASSWORD

    receiver = ("profesor.rosendo@gmail.com")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)


def news_about(topic):
    now = datetime.now().date().isoformat()

    api_key = NEWS_API_KEY
    url = (f"https://newsapi.org/v2/everything?"
           f"q={topic}&"
       "from={now}&"
           "sortBy=publishedAt&"
       f"apiKey={api_key}&"
           f"language=")

    # Make a request
    request = requests.get(url)

    # return a dictionary with data
    return request.json()
