import requests
import selectorlib
from send_email import send_email

URL = "http://programmer100.pythonanywhere.com/tours/"

message_info = """\
Subject: Hi!

New Event was found.
"""

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(info):
    with open("data.txt", "a") as file:
        file.write(info + "\n")


def read(data_info):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scrapped = scrape(URL)
    extracted = extract(scrapped)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message_info)
            print("new_email")

