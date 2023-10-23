import requests
import selectorlib


URL ="https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '39.0.2171.95 Safari/537.36'}

def scrapes (url):
    response = requests.get(url=url, headers=HEADERS)
    source = response.text
    return source

def extract (source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value

if __name__ == "__main__":
    scraped = scrapes(URL)
    extracted = extract(scraped)
    print(extracted)
