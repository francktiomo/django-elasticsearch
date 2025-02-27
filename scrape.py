import requests
from bs4 import BeautifulSoup
import json
import re

def clean_name(name):
    return re.sub(r",\s*\d{4}-\d{4}", "", name).strip()

def get_books() {
  infos = []

  for i in range(1, 501):
    info = {}
    # Fetch the page content
    url = f"https://www.gutenberg.org/ebooks/{i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    print(f"Scraping {url}")

    try:
      # Extract author
      author = soup.find("th", string="Author").find_next_sibling("td").text.strip()
      info['author'] = clean_name(author)

      # Extract title
      title = soup.find("th", string="Title").find_next_sibling("td").text.strip()
      info['title'] = title

      # # Extract summary
      summary = soup.find("th", string="Summary").find_next_sibling("td").text.strip()
      info['summary'] = summary

      infos.append(info)
    except Exception as e:
      continue
}

