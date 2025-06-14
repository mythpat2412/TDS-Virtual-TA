from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Optional: run in background

# ✅ Correct path to chromedriver
service = Service(r"C:\Users\Admin_Prasad\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the course page
driver.get("https://tds.s-anand.net/#/")

# Wait for content to load
time.sleep(3)

# Get page source
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract headings and content
headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
main_content = soup.find("body")
main_content_text = main_content.get_text(separator="\n", strip=True) if main_content else "No content found."

# ✅ Save to a file
with open("tds_scraped_content.txt", "w", encoding="utf-8") as f:
    f.write("Page Headings:\n")
    for heading in headings:
        f.write(f"- {heading}\n")
    f.write("\nMain Content:\n")
    f.write(main_content_text)

# Done
driver.quit()
print("✅ Scraped content saved to tds_scraped_content.txt")
