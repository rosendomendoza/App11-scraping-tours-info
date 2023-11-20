import sqlite3
import time
import requests
import selectorlib
from my_tools import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '39.0.2171.95 Safari/537.36'}


def scrapes(url):
    response = requests.get(url=url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value


def store(extracted):
    cursor = connection.cursor()
    elem = extracted.split(",")
    band, city, date = [elem[0].strip(), elem[1].strip(), elem[2].strip()]
    cursor.execute("INSERT INTO events VALUES(?,?,?)",
                   (band, city, date))
    connection.commit()

def readDB(extracted):
    cursor = connection.cursor()
    row = extracted.split(",")
    row = [elem.strip() for elem in row]
    band, city, date = row
    cursor.execute("SELECT * FROM events WHERE band=? AND city =? AND "
                   "date =?", (band, city, date))
    row = cursor.fetchall()
    return row


if __name__ == "__main__":
    connection = sqlite3.connect("data.db")
    while True:
        scraped = scrapes(URL)
        extracted = extract(scraped)

        if extracted != "No upcoming tours":
            if not readDB(extracted):
                store(extracted)
                message = f"""\
Subject: New Event
    
From: Scrapping APP
    
{extracted}
"""
                message = message.encode('utf-8')
                send_email(message)
                print(f"Next Tour: {extracted} sent it")
            else:
                print(f"Tour: {extracted} already reported")
        else:
            print("No upcoming Tours")
        time.sleep(2)
