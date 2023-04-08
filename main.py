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

    # Лайкает фото по хештегу
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
                self.put_exactly_like(url)
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # Проверяет наличие xpath
    def xpath_exist(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # Ставит лайк на конкретный пост
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
            print(f"Лайк на пост: {user_post} поставлен")

        # self.close_browser()

    # Собирает все посты с аккаунта в файл имя_аккаунта.txt
    def get_all_posts_urls(self, user_acc):
        browser = self.browser
        browser.get(user_acc)
        time.sleep(4)

        wrong_user_acc = "//span[contains(., 'К сожалению, эта страница недоступна.')]"
        if self.xpath_exist(wrong_user_acc):
            print("Такого пользователя не существует")
        else:
            print("Пользователь найден, ставим лайки")
            time.sleep(4)

            posts_count = int(
                browser.find_element(
                    By.XPATH,
                    "/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/span/span",
                ).text
            )
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, "a")
                hrefs = [
                    item.get_attribute("href")
                    for item in hrefs
                    if "/p/" in item.get_attribute("href")
                ]
                for href in hrefs:
                    posts_urls.append(href)
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(random.randrange(3, 5))
                print(f"Итерация #{i}")

            file_name = user_acc.split("/")[-2]
            posts_urls = list(set(posts_urls))

            with open(f"{file_name}.txt", "a") as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

    # Ставит лайки всем постам на аккаунте
    def put_many_likes(self, user_acc):
        browser = self.browser
        self.get_all_posts_urls(user_acc)
        file_name = user_acc.split("/")[-2]
        time.sleep(4)
        browser.get(user_acc)
        time.sleep(4)

        with open(f"{file_name}.txt") as file:
            urls_list = file.readlines()

            for url in urls_list[0:6]:
                try:
                    self.put_exactly_like(url)
                    time.sleep(5)
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # Скачивает контент со страницы пользователя
    def download_user_media(self, user_acc):
        pass

my_bot = InstagramBot(config.get("ACC_USERNAME"), config.get("ACC_PASSWORD"))
my_bot.login()
# my_bot.put_exactly_like("https://www.instagram.com/p/CqaENeks21L/")
my_bot.put_many_likes("https://www.instagram.com/tort.bar/")
