from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# Setup headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Load the course site
driver.get("https://tds.s-anand.net/#/")
time.sleep(5)  # Wait for JavaScript to render

# Extract HTML
html = driver.page_source
driver.quit()

# Parse and clean text
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text()
cleaned = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

# Save to data/tds_course.txt
os.makedirs("data", exist_ok=True)
with open("data/tds_course.txt", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Scraping complete. File saved to data/tds_course.txt")
