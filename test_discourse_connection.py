import requests
from bs4 import BeautifulSoup
import datetime

def scrape_discourse(start_date, end_date):
    print(f"Scraping posts from Discourse between {start_date} and {end_date}...")

    # Replace this with your Discourse URL
    base_url = "https://example.discourse.com/latest"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: extract post titles
    topics = []
    for topic in soup.find_all("a", class_="title"):
        title = topic.get_text(strip=True)
        url = topic.get("href")
        full_url = base_url + url if url.startswith("/") else url
        topics.append(f"{title} - {full_url}")

    return topics
