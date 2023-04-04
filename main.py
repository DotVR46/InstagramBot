from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import dotenv_values
import time
import random

config = dotenv_values(".env")


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(service=Service("chromedriver/chromedriver"))

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get("https://www.instagram.com/")
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element("name", "username")
        username_input.clear()
        username_input.send_keys(self.username)
        time.sleep(2)
        password_input = browser.find_element("name", "password")
        password_input.clear()
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    def like_photo_by_hashtag(self, hashtag):
        browser = self.browser
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))
        hrefs = browser.find_elements(By.TAG_NAME, "a")
        posts_urls = [
            item.get_attribute("href")
            for item in hrefs
            if "/p/" in item.get_attribute("href")
        ]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(5)
                like_button = browser.find_element(
                    By.XPATH, '//span/*[contains(@aria-label, "Нравится")]'
                )
                like_button.click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    def xpath_exist(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def put_exactly_like(self, user_post):
        browser = self.browser
        browser.get(user_post)
        time.sleep(4)

        wrong_user_post = "//span[contains(., 'К сожалению, эта страница недоступна.')]"
        if self.xpath_exist(wrong_user_post):
            print("Такого поста не существует")
        else:
            print("Пост найден, ставим лайк")
            time.sleep(4)
            like_button = '//span/*[contains(@aria-label, "Нравится")]'
            browser.find_element(By.XPATH, like_button).click()
            time.sleep(4)
            print(f"Лайк на пост: {user_post} поставлен")
        self.close_browser()


my_bot = InstagramBot(config.get("ACC_USERNAME"), config.get("ACC_PASSWORD"))
my_bot.login()
my_bot.put_exactly_like("https://www.instagram.com/p/CqaENeks21L/")

# def hashtag_search(username, password, hashtag):
#     browser = webdriver.Chrome(service=Service("chromedriver/chromedriver"))
#     try:
#         browser.get("https://www.instagram.com/")
#         time.sleep(random.randrange(3, 5))
#
#         username_input = browser.find_element("name", "username")
#         username_input.clear()
#         username_input.send_keys(username)
#         time.sleep(2)
#         password_input = browser.find_element("name", "password")
#         password_input.clear()
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.ENTER)
#         time.sleep(10)
#
#         try:
#             browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
#             time.sleep(5)
#
#             for i in range(1, 4):
#                 browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 # browser.implicitly_wait(random.randrange(3, 5))
#                 time.sleep(random.randrange(3, 5))
#             hrefs = browser.find_elements(By.TAG_NAME, "a")
#             posts_urls = [
#                 item.get_attribute("href")
#                 for item in hrefs
#                 if "/p/" in item.get_attribute("href")
#             ]
#
#             for url in posts_urls:
#                 try:
#                     browser.get(url)
#                     time.sleep(5)
#                     browser.implicitly_wait(15)
#                     like_button = browser.find_element(By.XPATH, '//span/*[contains(@aria-label, "Нравится")]').click()
#                     time.sleep(random.randrange(80, 100))
#                 except Exception as ex:
#                     print(ex)
#         except Exception as ex:
#             print(ex)
#     except Exception as ex:
#         print(ex)
#     finally:
#         browser.close()
#         browser.quit()


# login(config.get("ACC_USERNAME"), config.get("ACC_PASSWORD"))
# hashtag_search(config.get("ACC_USERNAME"), config.get("ACC_PASSWORD"), "росписьнаткани")
