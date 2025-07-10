from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

def test_title():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Ruta absoluta al chromedriver
    driver_path = os.path.abspath("chromedriver.exe")
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("http://127.0.0.1:8058/")
        time.sleep(2)
        assert "Dash" in driver.title
    finally:
        driver.quit()
