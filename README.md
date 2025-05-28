Цель проекта - создать парсер для сбора информации об оценках фильмов пользователями Кинопоиска. Полученные данные могут быть использованы для:

Анализа кинопредпочтений пользователей
Построения рекомендательных систем
Парсер должен:

Принимать username пользователя Кинопоиска
Собирать информацию о всех оцененных фильмах:
Название фильма
Год выпуска
Оценка пользователя
Сохранять данные в структурированном формате (JSON/CSV/Excel)

Инструкция по запуску

Требования

Python 3.8+
Установленные зависимости:
pip install requests beautifulsoup4 pandas fake-useragent

Запуск

Склонируйте репозиторий
Установите зависимости
Запустите скрипт:
from kinopoisk_parser import KinopoiskUserParser

parser = KinopoiskUserParser()
user_data = parser.parse_user_ratings(username='ваш_username')
parser.save_to_excel(user_data, 'output.xlsx')