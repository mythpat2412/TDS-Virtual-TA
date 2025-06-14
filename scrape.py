from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Optional: configure options (headless mode, etc.)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment if you don't want the browser to open

# Path to your downloaded and extracted chromedriver.exe
service = Service(r"C:\Users\Admin_Prasad\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# Start the driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Now you can navigate to the site and scrape
driver.get("https://tds.s-anand.net/#/")

# Optional: wait for content to load
time.sleep(3)

# Example: print page title
print(driver.title)

# Always close the browser when done
driver.quit()
