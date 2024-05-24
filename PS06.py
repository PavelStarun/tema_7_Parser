import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

url = 'https://www.divan.by/category/ortopedicheskie-divany-dlya-sna'
driver.get(url)
time.sleep(3)

divan_list = driver.find_elements(By.CLASS_NAME, 'WdR1o')

category = []

for divan in divan_list:
    try:
        title = divan.find_element(By.TAG_NAME, 'span').text
        price = divan.find_element(By.CLASS_NAME, 'q5Uds').text
        link = divan.find_element(By.TAG_NAME, 'a').get_attribute('href')

    except:
        print("Произошла ошибка при парсинге данных")
        continue

    category.append([title, price, link])

with open("divany_dlya_sna.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название дивана', 'Цена', 'Ссылка'])
    writer.writerows(category)




