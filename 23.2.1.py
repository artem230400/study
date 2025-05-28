import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import json
import time
from typing import List, Dict, Optional


class KinopoiskUserParser:
    BASE_URL = 'https://www.kinopoisk.ru/user'
    HEADERS = {
        'User-Agent': UserAgent().random,
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    def __init__(self, delay: float = 1.0):
        self.delay = delay 
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_page_content(self, url: str) -> Optional[str]:
        """Получение содержимого страницы с обработкой ошибок"""
        try:
            time.sleep(self.delay)
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

    def parse_user_ratings(self, username: str) -> List[Dict]:
        """Парсинг оценок пользователя"""
        page_num = 1
        ratings = []

        while True:
            url = f"{self.BASE_URL}/{username}/votes/list/ord/date/page/{page_num}/"
            html = self.get_page_content(url)

            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')
            items = soup.select('div.item')

            if not items:
                break

            for item in items:
                try:
                    title = item.select_one('div.name a').text.strip()
                    year = item.select_one('div.name div.text-grey').text.strip('()')
                    rating = item.select_one('div.vote div.rating').text.strip()

                    ratings.append({
                        'title': title,
                        'year': year,
                        'rating': rating,
                        'user': username
                    })
                except AttributeError as e:
                    continue

            page_num += 1

        return ratings

    def save_to_json(self, data: List[Dict], filename: str):
        """Сохранение в JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_to_csv(self, data: List[Dict], filename: str):
        """Сохранение в CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    def save_to_excel(self, data: List[Dict], filename: str):
        """Сохранение в Excel"""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)


if __name__ == '__main__':
    parser = KinopoiskUserParser()

    user_data = parser.parse_user_ratings(username='12345')  # Замените на реальный username

    if user_data:
        parser.save_to_json(user_data, 'kinopoisk_ratings.json')
        parser.save_to_csv(user_data, 'kinopoisk_ratings.csv')
        parser.save_to_excel(user_data, 'kinopoisk_ratings.xlsx')
        print(f"Успешно собрано {len(user_data)} оценок")
    else:
        print("Не удалось собрать данные")