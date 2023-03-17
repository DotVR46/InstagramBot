from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from dotenv import dotenv_values
import time
import random

config = dotenv_values(".env")


def login(username, password):
    browser = webdriver.Chrome(service=Service("chromedriver/chromedriver"))

    browser.get("https://www.instagram.com/")
    time.sleep(random.randrange(3, 5))

    browser.close()
    browser.quit()


login(config.get("ACC_USERNAME"), config.get("ACC_PASSWORD"))
