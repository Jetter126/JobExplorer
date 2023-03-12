from bs4 import BeautifulSoup
import csv
import requests
import random
import headers
import pandas as pd

# Enters search parameters into URL
def get_url(position, location):
    template = "https://ca.linkedin.com/jobs/search?keywords={}&location={}"
    url = template.format(position, location)
    return url

# Generate pieces of information from job listing
def get_info(card):
    card_position = card.find("h3", "base-search-card__title").text.strip()
    card_company = card.find("h4", "base-search-card__subtitle").a.text.strip()
    card_location = card.find("span", "job-search-card__location").text.strip()
    card_url = card.find("a", "base-card__full-link").get("href").strip()

    try:
        card_listdate = card.find("time", "job-search-card__listdate").text.strip()
    except AttributeError:
        card_listdate = "-"

    try:
        card_salary = card.find("span", "job-search-card__salary-info").text.strip()
    except AttributeError:
        card_salary = "-"

    info = (card_position, card_company, card_location, card_listdate, card_salary, card_url)
    return info

# Generate list of LinkedIn results
def generate_jobs(position, location):
    # Stores the list
    data = []

    # Passes parameters into LinkedIn URL for web scraping
    url = get_url(position, location)
    response = requests.get(url, headers=random.choice(headers.header_list))
    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("div", "base-card")

    # Adds data from each listing to the list
    for card in cards:
        info = get_info(card)
        data.append(info)

    with open("jobs.csv", "a+") as file:
        writer = csv.writer(file)
        writer.writerows(data)