import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
ua = UserAgent()
options.add_argument('--headless')
options.add_argument(f'user-agent={ua.chrome}')
options.add_argument('--disable-blink-features=AutomationControlled')


def get_url(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(2)

    catalog_news = driver.find_element(By.CLASS_NAME, value='rubric-page__container').find_element(By.CLASS_NAME,
                                                                                                   value='rubric-page__item')
    first_new = catalog_news.find_element(By.CLASS_NAME, value='card-full-news')
    return f"{catalog_news.text}\n{first_new.get_attribute('href')}"
