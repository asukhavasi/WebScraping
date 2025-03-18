import time
import requests
import selectorlib
import smtplib, ssl
import os
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("scrapedata.db")

def scrape(url):
    """Scrape the page source from URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)['tours']
    return value

def sendmail(message):

    host = 'smtp.gmail.com'
    port = 465

    username = 'asukhava@gmail.com'
    password = ''

    receiver = 'sukhavasiabilash@gmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host,port,context=context) as server:
        server.login(username,password)
        server.sendmail(username,receiver,message)

    print("Email is sent!")


def store_data(tourdetails):

    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("insert into events values(?,?,?)",row)
    connection.commit()


def read(extracted):

    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute("select * from events where band=? and city=? and "
                   "date=?",(band,city,date))
    rows = cursor.fetchall()
    return rows

if __name__ == "__main__":
    while True:
        output = scrape(URL)
        extracted = extract(output)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store_data(extracted)
                sendmail(extracted)
        time.sleep(2)



