import requests
from bs4 import BeautifulSoup as soup
from html.parser import HTMLParser
import time
import csv


class MyHTMLParser(HTMLParser):
    def __init__(self, use_list):
        super().__init__()
        self.use_list = use_list

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        pass

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        # print("Encountered some data  :", data)
        self.use_list.append(data)


def save_prices(data):
    csv_data = []
    with open("gas_prices/gas_prices.csv", "r", newline="") as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            csv_data.append(row)

    if not csv_data[-1][0] == f"{data[0][1]}-{data[0][2]}-{data[0][0]}":
        with open("gas_prices/gas_prices.csv", "w", newline="") as file:
            writer = csv.writer(file)

            for row in csv_data:
                writer.writerow(row)

            new_data = [f"{data[0][1]}-{data[0][2]}-{data[0][0]}"]
            for entry in data[1:]:
                new_data.append(entry[1])
            writer.writerow(new_data)
        print(f"\nSaved the gas prices at {time.asctime()}\n")
    else:
        print(f"\nAlready saved gas price data today ({data[0][1]}-{data[0][2]}-{data[0][0]})\n")


def gas_prices():
    # getting page html
    raw_html = requests.get("https://www.gasbuddy.com/USA").text

    # parsing page html
    page_parser = soup(raw_html, "html.parser")

    # getting the div tag with specific class from the raw html
    states_html = page_parser.body.findAll("div", {"class": "col-sm-6 col-xs-6 siteName"})
    prices_html = page_parser.body.findAll("div", {"class": "col-sm-2 col-xs-3 text-right"})

    # initializing empty lists for layer
    states_parsed, prices_parsed = [], []
    states, prices, combined = [], [], [time.gmtime()]

    # parsing the states html tags into data
    states_parser = MyHTMLParser(states_parsed)
    states_parser.feed(str(states_html))

    # parsing the prices html tags into data
    prices_parser = MyHTMLParser(prices_parsed)
    prices_parser.feed(str(prices_html))

    # adding states from html data into list
    for state in states_parsed:
        if states_parsed.index(state) % 2:
            states.append(state.lstrip('\r\n                                ').rstrip('\r\n                            ').lower())

    # adding prices from html data into list
    for price in prices_parsed:
        if prices_parsed.index(price) % 2:
            prices.append(float(price.lstrip('\r\n                                ').rstrip('\r\n                            ')))

    # combining states and prices into a tuple for each state
    for i in range(len(prices)):
        temp = [states[i], prices[i]]
        combined.append(tuple(temp))

    return combined

