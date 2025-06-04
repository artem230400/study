import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
from typing import List, Dict, Optional


class KinopoiskUserParser:
    BASE_URL = 'https://www.kinopoisk.ru/community/interest/397/?ysclid=mbhqlvgzn1759987534'
    HEADERS = {
        'User-Agent': UserAgent().random,
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_page_content(self, url: str) -> Optional[str]:
        try:
            time.sleep(self.delay)
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

    def parse_user_ratings(self, username: str) -> List[Dict]:
        page_num = 1
        ratings = []

        while True:
            url = f"{self.BASE_URL}/{username}/votes/list/ord/date/page/{page_num}/"
            print(f"Парсинг страницы {page_num}...")

            html = self.get_page_content(url)
            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')
            film_blocks = soup.select('div.profileFilmsList > div.item')

            if not film_blocks:
                break

            for film in film_blocks:
                try:
                    title_elem = film.select_one('div.nameRus > a')
                    title = title_elem.text.strip() if title_elem else "Нет названия"

                    year_elem = film.select_one('div.nameRus > span')
                    year = year_elem.text.strip('() ') if year_elem else "Нет года"

                    rating_elem = film.select_one('div.vote div.rating')
                    rating = rating_elem.text.strip() if rating_elem else "Нет оценки"

                    print(f"Найден фильм: {title} ({year}), оценка: {rating}")

                    ratings.append({
                        'title': title,
                        'year': year,
                        'rating': rating,
                        'user': username
                    })
                except Exception as e:
                    print(f"Ошибка при парсинге блока фильма: {e}")
                    continue

            page_num += 1

        return ratings

    def save_to_json(self, data: List[Dict], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_to_csv(self, data: List[Dict], filename: str):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    def save_to_excel(self, data: List[Dict], filename: str):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)


if __name__ == '__main__':
    parser = KinopoiskUserParser(delay=3.0)

    user_data = parser.parse_user_ratings(username='245477')

    if user_data:
        print(f"\nУспешно собрано {len(user_data)} оценок:")
        for i, item in enumerate(user_data[:5], 1):
            print(f"{i}. {item['title']} ({item['year']}) - {item['rating']}")

        parser.save_to_json(user_data, 'kinopoisk_ratings.json')
        parser.save_to_csv(user_data, 'kinopoisk_ratings.csv')
        parser.save_to_excel(user_data, 'kinopoisk_ratings.xlsx')
        print("\nДанные сохранены в файлы:")
        print("- kinopoisk_ratings.json")
        print("- kinopoisk_ratings.csv")
        print("- kinopoisk_ratings.xlsx")
    else:
        print("Не удалось собрать данные. Проверьте username и доступность страницы.")