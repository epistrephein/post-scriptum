"""Fetch articles from Il Post online newspaper (Italy section) and save them as JSON."""

import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ilpost.it/italia/page/{page}/"
FILENAME = "data/dataset.json"

MAX_PAGE = 500
MAX_YEAR = 2023
MIN_YEAR = 2018

ARTICLE_CSS_SELECTOR = 'div[class*="index_home-left"]'
ARTICLE_DATE_REGEX = re.compile(r'/(\d{4})/(\d{2})/(\d{2})/')

# Check if JSON file already exists and prompt user for overwrite
if os.path.exists(FILENAME):
    if input(f"💬 File {FILENAME} already exists. Overwrite? [y/N] ") != 'y':
        print("❌ Not overwriting: aborting")
        exit()

# Initialize variables
results = []
page = 1
finished = False

while page < MAX_PAGE:
    # Construct the URL for the current page number
    url = BASE_URL.format(page=page)

    # Fetch the page
    response = requests.get(url, timeout=30)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"❌ Failed to fetch page {url}: aborting")
        break

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'lxml')

    # Select the container containing the articles and grab them all
    container = soup.select(ARTICLE_CSS_SELECTOR)
    articles = container[0].find_all('article')

    # Iterate articles
    for article in articles:
        # Extract title and URL
        main_content = article.find('a')
        article_title = main_content.find('h2')
        article_url = main_content['href']

        # Check that all data is present
        date_match = ARTICLE_DATE_REGEX.search(article_url)
        if not article_title:
            print(f"❌ [{page}] Could not find title in {article_url}: skipping")
            continue
        elif not date_match:
            print(f"❌ [{page}] Could not find date in {article_url}: skipping")
            continue

        # Extract article date from URL
        extracted_date = '-'.join(date_match.groups())

        # Skip article if too new and stop if too old
        year = int(date_match[1])
        if year > MAX_YEAR:
            print(f"⏩️ [{page}] Article newer than {MAX_YEAR}: skipping")
            continue
        elif year < MIN_YEAR:
            print(f"🛑 [{page}] Article older than {MIN_YEAR}: finished")
            finished = True
            break

        # Append article to the list of results
        results.append((extracted_date, article_title.text, article_url))
        print(f"✅ [{page}] {extracted_date}: {article_title.text}")

    # Write data to file
    with open(FILENAME, 'w', encoding='utf-8') as infile:
        json.dump(results, infile, indent=4, ensure_ascii=False)

    print(f"💾 Saved to {FILENAME}")

    # Break from outer loop if oldest year was reached
    if finished:
        break

    # Increment page number
    page += 1

    # Sleep a little before the next request
    time.sleep(0.25)
