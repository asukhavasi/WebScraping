import time

import requests
import selectorlib
from datetime import datetime
import streamlit as st
import plotly.express as px
import pandas
import sqlite3



URL = "https://programmer100.pythonanywhere.com/"
connection = sqlite3.connect('scrapeweather.db')


def scrape(url):
    response = requests.get(url)
    tempdata = response.text
    return tempdata


def extract(data):
    extractdata = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractdata.extract(data)["temp"]
    return value

# def storeheader(data):
#     with open("tempdatacapture.txt",'a') as file:
#         file.write(data)


# def storebody(output):
#     now = datetime.now()
#     date_time = now.strftime("%y-%m-%d-%H-%M-%S")
#     write_data = f"{date_time},{output}\n"
#     with open("tempdatacapture.txt","a") as file:
#         file.write(write_data)


def store(temp):
    now = datetime.now()
    date_time = now.strftime("%y-%m-%d-%H-%M-%S")

    cursor = connection.cursor()
    cursor.execute("insert into weather values(?,?)",(date_time,temp))
    connection.commit()


def readtable():

    cur = connection.cursor()
    cur.execute("Select * from weather")
    rows = cur.fetchall()
    return rows


# def read():
#     with open("tempdatacapture.txt",'r') as file:
#         filedata = file.read()
#         return filedata

if __name__ == "__main__":
    # header = "date, temperature" + "\n"
    # cycle = 10
    # i=1
    # while i < cycle:
    #     source = scrape(URL)
    #     output = extract(source)
    #     headercheck = read()
    #     if header not in headercheck:
    #         storeheader(header)
    #     storebody(output)
    #     i+=1

    cycle = 10
    i=1
    while i < cycle:
        source = scrape(URL)
        output = extract(source)

        store(output)

        i+=1
        time.sleep(5)

    data = readtable()
    date = []
    temp = []
    i=0
    while i < len(data):
        date.append(data[i][0])
        temp.append(data[i][1])
        i+=1

    st.title("This is temperature flow for last 10 runs")
    fig = px.line(x=date,y=temp,
                  labels={"x":"Date","y":"Temperature(C)"})
    st.plotly_chart(fig)
