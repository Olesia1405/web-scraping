import requests
from bs4 import BeautifulSoup

# Список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# URL страницы со свежими статьями
URL = 'https://habr.com/ru/articles/'

# Заголовки для HTTP-запроса
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def fetch_articles(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

def parse_articles(html, keywords):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')
    suitable_articles = []

    for article in articles:
        preview = article.find('div', class_='article-formatted-body')
        if preview and any(keyword in preview.get_text().lower() for keyword in keywords):
            date = article.find('time')['datetime'].split('T')[0]
            title = article.find('a', class_='tm-article-snippet__title-link').text.strip()
            link = article.find('a', class_='tm-article-snippet__title-link')['href']
            suitable_articles.append((date, title, f'https://habr.com{link}'))
    
    return suitable_articles

def main():
    html = fetch_articles(URL, HEADERS)
    if html:
        articles = parse_articles(html, KEYWORDS)
        for date, title, link in articles:
            print(f'{date} – {title} – {link}')

if __name__ == '__main__':
    main()
