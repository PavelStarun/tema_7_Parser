from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time


def get_article_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find(id='firstHeading').text
        return title
    except Exception as e:
        return "Не удалось найти заголовок статьи."


request = input("Введите, что вы хотите найти на сайте Wikipedia?: ")

while True:
    print("Перейти по вашему запросу? 1-перейти, 2-выйти")
    choice = input().strip().lower()

    if choice == '1':
        print("Пожалуйста, подождите...\n")
        browser = webdriver.Chrome()
        browser.get('https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')
        search_box = browser.find_element(By.ID, 'searchInput')
        search_box.send_keys(request)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        print("Заголовок статьи:", get_article_title(browser.current_url))

        while True:
            print("\n1. Листать параграфы с этой статьи. \n2. Перейти на одну из связанных ссылок. \n3. Выйти")
            choice = input("Введите ваш выбор: ").strip()
            if choice == '1':
                print("Пожалуйста, подождите...\n")
                paragraphs = browser.find_elements(By.TAG_NAME, 'p')
                for paragraph in paragraphs:
                    print(paragraph.text)
                    print("\n1. Продолжить листание параграфов\n2. Перейти на одну из ссылок в этом параграфе\n3. Выйти")
                    action = input("Введите ваш выбор: ").strip()
                    if action == '':
                        print("Ошибка: Пустой ввод не допускается.")
                    elif action == '1':
                        continue
                    elif action == '2':
                        print("Пожалуйста, подождите...\n")
                        links = paragraph.find_elements(By.TAG_NAME, 'a')
                        valid_links = [link for link in links if link.get_attribute('href') and 'wikipedia.org' in link.get_attribute('href')]
                        if not valid_links:
                            print("Не удалось найти ссылки в этом параграфе.")
                            continue

                        print("Список ссылок в этом параграфе:")
                        for i, link in enumerate(valid_links):
                            link_url = link.get_attribute('href')
                            link_title = get_article_title(link_url)
                            print(f"{i + 1}. {link_title} - {link_url}")

                        link_choice = input("Введите номер ссылки для перехода или 'n' для остановки: ").strip()
                        if link_choice == '':
                            print("Ошибка: Пустой ввод не допускается.")
                        elif link_choice.lower() == 'n':
                            continue
                        else:
                            print("Пожалуйста, подождите...\n")
                            try:
                                link_index = int(link_choice) - 1
                                if 0 <= link_index < len(valid_links):
                                    new_url = valid_links[link_index].get_attribute('href')
                                    browser.get(new_url)
                                    time.sleep(3)
                                    print("Заголовок статьи:", get_article_title(browser.current_url))
                                    break
                                else:
                                    print("Неверный выбор")
                            except ValueError:
                                print("Неверный выбор")

                    elif action == '3':
                        browser.quit()
                        print("Завершение работы.")
                        exit()
                    else:
                        print("Неверный выбор")

            elif choice == '2':
                print("Эта опция доступна только при листании параграфов.")
            elif choice == '3':
                browser.quit()
                print("Завершение работы.")
                exit()
            else:
                print("Неверный выбор")

    elif choice == '2':
        print("Завершение работы.")
        break

    else:
        print("Неверный выбор")
