from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Selenium Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode

# Path to your ChromeDriver
driver_path = "path_to_chromedriver"  # Update this

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://tds.s-anand.net/#/"
driver.get(url)

# Wait for page to load JS
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
question_divs = soup.find_all('div', class_='question')

# Save all questions and answers
with open("tds_questions.txt", "w", encoding="utf-8") as f:
    for div in question_divs:
        f.write(div.get_text(separator="\n", strip=True) + "\n\n")

driver.quit()
