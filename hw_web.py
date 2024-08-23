import requests
from bs4 import BeautifulSoup

# Список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со свежими статьями
URL = 'https://habr.com/ru/articles/'

# Заголовки для HTTP-запроса
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Отправляем HTTP-запрос и получаем HTML-код страницы
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все статьи на странице
articles = soup.find_all('article', class_='post post_preview')

# Список подходящих статей
suitable_articles = []

# Перебираем все статьи
for article in articles:
    # Находим preview-информацию статьи
    preview = article.find('div', class_='post__text post__text-html js-mediator-article')

    # Если preview найден, проверяем на наличие ключевых слов
    if preview:
        text = preview.get_text().lower()
        for keyword in KEYWORDS:
            if keyword.lower() in text:
                # Находим дату, заголовок и ссылку статьи
                date = article.find('span', class_='post__time').text.strip()
                title = article.find('a', class_='post__title_link').text.strip()
                link = article.find('a', class_='post__title_link')['href']

                # Добавляем статью в список подходящих статей
                suitable_articles.append((date, title, link))
                break

# Выводим список подходящих статей
for date, title, link in suitable_articles:
    print(f'{date} – {title} – https://habr.com{link}')