from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def search_wikipedia(request):
    print("Пожалуйста, подождите...")
    browser = webdriver.Chrome()
    browser.get('https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')
    search_box = browser.find_element(By.NAME, 'search')
    search_box.send_keys(request)
    search_box.send_keys(Keys.ENTER)
    return browser


def browse_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, 'p')
    for paragraph in paragraphs:
        print(paragraph.text)
        print("1. Продолжить листание параграфов\n2. Перейти на одну из связанных ссылок\n3. Выйти")
        action = input("Введите ваш выбор: ").strip()
        if action == '1':
            continue
        elif action == '2':
            browse_links(browser)
            break
        elif action == '3':
            return False
        else:
            print("Неверный выбор")
    return True


def browse_links(browser):
    links = browser.find_elements(By.TAG_NAME, 'a')
    for link in links:
        print(link.get_attribute('href'))
        input("Нажмите Enter для продолжения...")


find = True
while find:
    request = input("Введите, что вы хотите найти на сайте Wikipedia?: ")
    print("Перейти по вашему запросу?  y/n/p (y-перейти и закончить сессию, p-продолжить, n-выйти)")
    choice = input().strip().lower()

    if choice == 'y':
        browser = search_wikipedia(request)
        browser.quit()
        find = False

    elif choice == 'p':
        browser = search_wikipedia(request)
        print("Выберите действия: \n1. Листать параграфы с этой статьи. \n2. Перейти на одну из связанных ссылок. \n3. Выйти")
        action = input("Введите ваш выбор: ").strip()

        if action == '1':
            if not browse_paragraphs(browser):
                find = False
        elif action == '2':
            browse_links(browser)
        elif action == '3':
            find = False
        else:
            print("Неверный выбор")

        browser.quit()

    elif choice == 'n':
        find = False
    else:
        print("Неверный выбор")

print("Завершение работы.")
