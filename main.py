import time
import sqlite3
import requests
import selectorlib
from send_email import send_email

connection = sqlite3.connect("data.db")

URL = "http://programmer100.pythonanywhere.com/tours/"

"INSERT INTO events VALUES ('Tigers', 'Tiger City', '2088.10.14')"

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
    row = info.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(data_info):
    row = data_info.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)

        if extracted != "No upcoming tours":
            rows = read(extracted)
            if not rows:
                store(extracted)
                send_email(message_info)
        time.sleep(2)
