import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Создаем экземпляр переводчика
translator = Translator()


# Функция для получения случайного английского слова и его определения
def get_english_words():
    url = "https://randomword.com/"  # Ссылка на сайт со случайными словами
    try:
        response = requests.get(url)  # Отправляем запрос на сайт
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")  # Парсим HTML
            english_word = soup.find("div", id="random_word").text.strip()  # Извлекаем слово
            word_definition = soup.find("div", id="random_word_definition").text.strip()  # Извлекаем определение
            # Пытаемся перевести слово и определение
            try:
                translated_word = translator.translate(english_word, src="en", dest="ru").text
                translated_definition = translator.translate(word_definition, src="en", dest="ru").text
            except Exception as e:
                print("Ошибка перевода:", e)
                translated_word, translated_definition = english_word, word_definition  # В случае ошибки используем оригинальные данные
            return {
                "original_word": english_word,
                "translated_word": translated_word,
                "translated_definition": translated_definition
            }
        else:
            print("Ошибка запроса: HTTP", response.status_code)  # Обработка ответа от сервера, который не 200 OK
            return None
    except Exception as e:
        print("Произошла ошибка при запросе:", e)
        return None


# Функция игры, где пользователь должен угадать слово
def word_game():
    print("Добро пожаловать в игру")  # Приветствие
    while True:
        word_info = get_english_words()
        if word_info is None:
            print("Не удалось получить слово, попробуйте еще раз позже.")
            continue  # Если не удалось получить слово, предлагаем повторить попытку

        translated_word = word_info['translated_word']
        translated_definition = word_info['translated_definition']

        print(f"Значение слова - {translated_definition}")  # Выводим определение на русском
        user_guess = input("Что это за слово? ")  # Просим пользователя ответить

        if user_guess.lower() == translated_word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {translated_word}")

        play_again = input("Хотите сыграть еще раз? д/н ")
        if play_again.lower() != 'д':
            print("Спасибо за игру!")
            break


word_game()  # Запускаем игру
