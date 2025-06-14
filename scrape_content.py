import requests
from bs4 import BeautifulSoup

def scrape_tds_course():
    url = "https://tds.s-anand.net/#/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text from the page
    text = soup.get_text(separator="\n")
    return text

# Usage
course_text = scrape_tds_course()
with open("tds_course.txt", "w", encoding="utf-8") as f:
    f.write(course_text)
