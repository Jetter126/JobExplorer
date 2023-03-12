from bs4 import BeautifulSoup
import csv
import requests
import random
import headers
import pandas as pd

# Enters search parameters into URL
def get_url(position, location):
    template = "https://www.simplyhired.com/search?q={}&l={}"
    url = template.format(position, location)
    return url

# Change the formatting of the posted date
def date_format(date):
    if date == "-":
        return "-"
    elif "h" in date:
        return date[:-1] + " hours ago"
    elif "d" in date:
        return date[:-1] + " days ago"
    if "m" in date:
        return date[:-1] + " months ago"
    else:
        return date[:-1] + " years ago"

# Generate pieces of information from job listing
def get_info(card):
    try:
        card_position = card.find("a", "chakra-button").text.strip()
    except AttributeError:
        return False
    try:
        card_company = card.find("span", {"data-testid": "companyName"}).text.strip()
    except AttributeError:
        return False
    try:
        card_location = card.find("span", {"data-testid": "searchSerpJobLocation"}).text.strip()
    except AttributeError:
        return False    
    try: 
        card_url = "https://www.simplyhired.com" + card.find("a", "chakra-button").get("href").strip()
    except AttributeError:
        return False
    try:
        card_listdate = card.find("p", {"data-testid": "searchSerpJobDateStamp"}).text.strip()
    except AttributeError:
        card_listdate = "-"
    card_listdate = date_format(card_listdate)
    try:
        card_salary = card.find("p", {"data-testid": "searchSerpJobSalaryEst"}).text.strip()
    except AttributeError:
        card_salary = "-"

    info = (card_position, card_company, card_location, card_listdate, card_salary, card_url)
    return info

# Generate list of SimplyHired results
def generate_jobs(position, location):
    # Stores the list
    data = []

    # Passes parameters into SimplyHired URL for web scraping
    url = get_url(position, location)
    response = requests.get(url, headers=random.choice(headers.header_list))
    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("li", "css-0")

    # Adds data from each listing to the list
    for card in cards:
        print(get_info(card))
        if get_info(card):
            info = get_info(card)
            data.append(info)

    print(data)

    with open("jobs.csv", "a+") as file:
        writer = csv.writer(file)
        writer.writerows(data)